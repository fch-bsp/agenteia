import os
import glob
import sqlite3
import json
import yaml
from flask import Flask, request, jsonify

# LangChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.docstore.document import Document
from langchain.schema import SystemMessage, HumanMessage

# Arquivo de configuração
CONFIG_FILE = "config.yaml"
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

# Lê chave openai e armazena em variável de ambiente
os.environ["OPENAI_API_KEY"] = config["api_key"]["key"]

# Nome do banco de dados para dados de suporte
DATABASE_PATH = "bsp.db"

# Flask
app = Flask(__name__)

# Memória e Contexto, usa Dicionário do Python
client_memories = {}  # conversa
client_context = {}  # número do atendimento do cliente - pode não ser usado

# Conecta com bd e retorna dados como dicionário
def get_db_connection():
    """Conecta ao banco de dados e configura para retornar dicionários."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

# carrega documentos e retorna uma lista 
def load_documents(folder_path):
    """Carrega documentos TXT da pasta indicada e retorna uma lista de Documentos."""
    documents = []
    for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": filepath}))
    return documents

# Carrega os documentos 
documents = load_documents("documents")

# Cria vectorstore com FAISS
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(documents, embeddings)

# Inicializa o modelo de chat com a mensagem do sistema
# Temperatura zero = respostas determinísticas
model = config["model"]["name"]
chat = ChatOpenAI(model=model, temperature=0)

# Definir o comportamento do agente
system_message = SystemMessage(content=(
    "Você é um assistente virtual especializado em RH que fornece informações sobre os funcionários. "
    "Sua função é responder perguntas sobre os funcionários, suas certificações, especialidades e outras informações relevantes. "
    "Responda sempre de maneira clara e objetiva, priorizando a precisão das informações. "
    "Caso a pergunta não esteja relacionada aos funcionários ou às informações disponíveis, "
    "responda: 'Desculpe, mas não posso responder a esse tipo de pergunta.'"
))

# Cria o retriever a partir do vectorstore
retriever = vectorstore.as_retriever()

# Avaliação se é consulta sobre funcionário através de LLM
def avaliar_consulta(question):
    system_prompt = (
        "Você é um assistente que analisa perguntas para determinar se elas se referem a algum funcionário. "
        "Se a pergunta for sobre funcionário, extraia o nome do funcionário se presente e identifique o tipo de consulta, "
        "que pode ser: 'data_nascimento', 'certificacoes', 'especialidade', 'descricao'. "
        "Caso a pergunta não seja sobre funcionário, retorne is_funcionario como false. "
        "Sua resposta DEVE ser **exclusivamente** um JSON válido, sem qualquer texto adicional, no seguinte formato: "
        '{"is_funcionario": <true ou false>, "nome_funcionario": <nome ou null>, "consulta": <"data_nascimento", "certificacoes", "especialidade", "descricao" ou null>}.'
    )
    human_prompt = f"Pergunta: \"{question}\""
    response = chat([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    response_content = response.content.strip()
    return json.loads(response_content)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or "client_id" not in data or "question" not in data:
        return jsonify({"error": "Requisição inválida. Forneça 'client_id' e 'question'."}), 400

    client_id = data["client_id"]
    question = data["question"]

    # Verifica se é sobre funcionário usando LLM
    funcionario_info = avaliar_consulta(question)
    if funcionario_info.get("is_funcionario"):
        nome_funcionario = funcionario_info.get("nome_funcionario")
        consulta = funcionario_info.get("consulta")
        
        # Se nome do funcionário não foi identificado, tenta usar o último contexto salvo
        if not nome_funcionario and client_id in client_context:
            nome_funcionario = client_context[client_id]
        if not nome_funcionario:
            return jsonify({"answer": "Por favor, informe o nome do funcionário para que eu possa buscar as informações."})
        
        # Consulta o banco de dados pelo nome do funcionário
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM atendimentos WHERE nome_funcionario LIKE ?", (f"%{nome_funcionario}%",))
        funcionario = cursor.fetchone()
        if funcionario:
            client_context[client_id] = nome_funcionario  # atualiza o contexto do cliente
            if consulta == "data_nascimento":
                answer = f"A data de nascimento de {funcionario['nome_funcionario']} é: {funcionario['data_nascimento']}."
            elif consulta == "certificacoes":
                answer = f"As certificações de {funcionario['nome_funcionario']} são: {funcionario['certificacoes']}."
            elif consulta == "especialidade":
                answer = f"A especialidade de {funcionario['nome_funcionario']} é: {funcionario['especialidade']}."
            elif consulta == "descricao":
                answer = f"Sobre {funcionario['nome_funcionario']}: {funcionario['descricao']}."
            else:
                answer = f"Funcionário: {funcionario['nome_funcionario']}\nData de Nascimento: {funcionario['data_nascimento']}\nCertificações: {funcionario['certificacoes']}\nEspecialidade: {funcionario['especialidade']}\nDescrição: {funcionario['descricao']}"
        else:
            answer = f"Não encontrei informações sobre o funcionário {nome_funcionario}. Verifique se o nome está correto."
        return jsonify({"answer": answer})
    
    # Se não for sobre funcionário, segue com a cadeia padrão
    if client_id not in client_memories:
        client_memories[client_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory = client_memories[client_id]
    
    # Cria a cadeia de conversação com Retrieval
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=retriever,
        memory=memory
    )

    # Executa a cadeia com a pergunta do usuário
    result = qa_chain.invoke({"question": question})
    answer = result.get("answer", "")

    return jsonify({"answer": answer})

if __name__ == '__main__':
    # Servidor Flask na porta 5000
    app.run(port=5000, debug=True)