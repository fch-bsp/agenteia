# verificador_documentos.py
# Execute este script separadamente para verificar a existência e conteúdo dos arquivos
import os
import sys

def verificar_documentos(pasta="documents"):
    """Verifica se os arquivos existem e exibe informações sobre eles"""
    print("\n" + "="*50)
    print(f"VERIFICADOR DE DOCUMENTOS - Pasta: {pasta}")
    print("="*50)
    
    # Verificar existência da pasta
    if not os.path.exists(pasta):
        print(f"ERRO: A pasta '{pasta}' não existe!")
        
        # Verificar diretório atual
        diretorio_atual = os.getcwd()
        print(f"Diretório atual: {diretorio_atual}")
        
        # Listar conteúdo do diretório atual
        print("\nConteúdo do diretório atual:")
        for item in os.listdir(diretorio_atual):
            print(f"  - {item}")
        
        return
    
    # Listar todos os arquivos na pasta
    arquivos = os.listdir(pasta)
    print(f"\nTotal de arquivos encontrados: {len(arquivos)}")
    
    # Verificar especificamente os arquivos txt
    arquivos_txt = [f for f in arquivos if f.endswith('.txt')]
    print(f"Arquivos .txt encontrados: {len(arquivos_txt)}")
    
    for arquivo in arquivos_txt:
        caminho_completo = os.path.join(pasta, arquivo)
        tamanho = os.path.getsize(caminho_completo)
        
        # Verificar se é o arquivo problemático
        destaque = " <-- ARQUIVO BUSCADO" if arquivo == "service_aws.txt" else ""
        
        print(f"\nArquivo: {arquivo}{destaque}")
        print(f"  - Caminho: {caminho_completo}")
        print(f"  - Tamanho: {tamanho} bytes")
        
        # Tentar ler primeiras linhas do arquivo
        try:
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                inicio = f.read(100)
                print(f"  - Primeiras 100 letras: {inicio.replace(chr(10), ' ').replace(chr(13), ' ')}...")
        except Exception as e:
            print(f"  - ERRO ao ler arquivo: {e}")
    
    # Verificar especificamente o arquivo service_aws.txt
    arquivo_aws = "service_aws.txt"
    caminho_aws = os.path.join(pasta, arquivo_aws)
    
    if os.path.exists(caminho_aws):
        print(f"\nO arquivo '{arquivo_aws}' EXISTE no diretório!")
        
        # Verificar se é realmente um arquivo
        if os.path.isfile(caminho_aws):
            print("É um arquivo regular.")
        else:
            print("ALERTA: Não é um arquivo regular!")
            
        # Verificar permissões
        if os.access(caminho_aws, os.R_OK):
            print("O arquivo tem permissão de leitura.")
        else:
            print("ALERTA: O arquivo NÃO tem permissão de leitura!")
    else:
        print(f"\nO arquivo '{arquivo_aws}' NÃO EXISTE no diretório!")
        
        # Verificar se existe algum arquivo com nome similar
        arquivos_similares = [f for f in arquivos if "aws" in f.lower() or "service" in f.lower()]
        if arquivos_similares:
            print(f"Arquivos com nomes similares encontrados: {arquivos_similares}")

if __name__ == "__main__":
    # Se uma pasta for fornecida como argumento, use-a
    pasta = sys.argv[1] if len(sys.argv) > 1 else "documents"
    verificar_documentos(pasta)
    
    # Verificar também no diretório atual
    if pasta != ".":
        verificar_documentos(".")
        
    # Verificar no diretório do script
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_documents = os.path.join(diretorio_script, "documents")
    
    if pasta != pasta_documents:
        verificar_documentos(pasta_documents)