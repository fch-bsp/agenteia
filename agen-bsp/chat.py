import streamlit as st
import requests
import uuid
import time

# Configuração da página
st.set_page_config(
    page_title="BSPCLOUD IA Assistente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove menu hamburger e footer
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Header fixo */
    .header-fixed {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #1976D2, #2196F3);
        z-index: 9999;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-bottom-left-radius: 1.5rem;
        border-bottom-right-radius: 1.5rem;
        margin: 0 1rem;
        width: calc(100% - 2rem);
    }

    /* Ajuste das cores do texto para o fundo azul */
    .header-fixed .title {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    .header-fixed .subtitle {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.4rem !important;
    }

    /* Área de chat */
    .chat-area {
        margin-top: 250px;  /* Espaço para o header fixo */
        padding: 1rem;
        height: calc(100vh - 300px);
        overflow-y: auto;
    }

    /* Mensagens */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease;
    }

    .user-message {
        background: #E3F2FD;
        margin-left: 2rem;
    }

    .assistant-message {
        background: #FFF8E1;
        margin-right: 2rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Título e subtítulo */
    .title {
        color: white;
        font-size: 2rem;
        margin: 1rem 0;
        font-weight: 600;
    }

    .subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.4rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# Header fixo
st.markdown("""
    <div class='header-fixed'>
        <img src='bsp.png' style='width:180px; display:block; margin:0 auto;'>
        <h1 class='title'>BSPCLOUD IA Assistente</h1>
        <p class='subtitle'>Como posso ajudar você hoje?</p>
    </div>
""", unsafe_allow_html=True)

# Inicialização do estado
if "client_id" not in st.session_state:
    st.session_state.client_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

def ask_question(question):
    url = "http://127.0.0.1:5000/ask"
    payload = {
        "client_id": st.session_state.client_id,
        "question": question
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("answer", "Desculpe, não consegui processar sua pergunta.")
        return f"Erro na comunicação com o servidor: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Não foi possível conectar ao servidor. Verifique se o backend está rodando."
    except requests.exceptions.Timeout:
        return "O servidor demorou muito para responder. Tente novamente."
    except Exception as e:
        return f"Ocorreu um erro inesperado: {str(e)}"

# Área de chat com scroll
st.markdown("<div class='chat-area'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_style = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f"<div class='chat-message {role_style}'>{message['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input do usuário
prompt = st.chat_input("💭 Digite sua mensagem aqui...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner('Processando sua mensagem...'):
        answer = ask_question(prompt)
        time.sleep(0.5)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()