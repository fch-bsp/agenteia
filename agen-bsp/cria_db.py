import sqlite3

DB_NAME = "bsp.db"

def create_database():
    """Cria o banco de dados SQLite e a tabela de atendimentos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Apaga a tabela se já existir para evitar conflitos de schema
    cursor.execute('DROP TABLE IF EXISTS atendimentos')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_funcionario TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            certificacoes TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_sample_data():
    """Insere registros de funcionários no banco de dados."""
    funcionarios = [
        # Funcionários originais
        (
            "Fernando Carlos", "29/03/1981", "AWS-Practitioner, AWS-Solutions Architect Associate", 
            "Líder técnico responsável por liderar uma vertical com Analistas AWS", 
            "Com mais de 5 anos de experiência como arquiteto de soluções na AWS, tenho atuado de forma estratégica na criação, implantação e otimização de ambientes em nuvem, sempre com foco em performance, segurança e escalabilidade."
        ),
        (
            "Maria Silva", "15/07/1988", "AWS-Solutions Architect, Azure-Developer, CompTIA Security+", 
            "Arquiteta de soluções cloud", 
            "Especialista em arquiteturas multi-cloud com foco em alta disponibilidade e segurança. Possui expertise em implementações híbridas entre AWS e Azure."
        ),
        (
            "Carlos Oliveira", "22/11/1990", "GCP-Professional Cloud Architect, Certified Kubernetes Administrator", 
            "Especialista em Big Data", 
            "Experiência com implementação de soluções de processamento de dados em larga escala usando ferramentas do Google Cloud Platform e orquestração de containers com Kubernetes."
        ),
        
        # Novos funcionários
        (
            "Ana Pereira", "05/04/1985", "AWS-DevOps Engineer, Terraform Certified Associate, GitLab Certified", 
            "DevOps Specialist", 
            "Profissional com 8 anos de experiência em práticas de DevOps, especializada em pipeline CI/CD e infraestrutura como código. Liderou a transformação de processos manuais para automação completa, reduzindo o tempo de deploy em 70%."
        ),
        (
            "Lucas Santos", "18/09/1993", "Azure-Administrator, Azure-Security Engineer, CISSP", 
            "Especialista em Segurança Cloud", 
            "Focado em proteção de dados e conformidade no ambiente Azure. Implementou controles de segurança que reduziram em 45% os incidentes de segurança e garantiu certificação LGPD para todos os sistemas da empresa."
        ),
        (
            "Juliana Costa", "27/12/1984", "Oracle Database Administrator, MongoDB Professional, Redis Certified Developer", 
            "Database Administrator Senior", 
            "Especialista em bancos de dados relacionais e NoSQL com 12 anos de experiência. Otimizou consultas complexas reduzindo o tempo de resposta em 60% e implementou estratégias de sharding para clusters MongoDB que suportam mais de 20TB de dados."
        ),
        (
            "Roberto Almeida", "03/06/1979", "ITIL Expert, PMP, SAFe Agilist", 
            "Gerente de Projetos de TI", 
            "Mais de 15 anos liderando projetos de transformação digital para grandes empresas. Coordenou equipes internacionais e implementou metodologias ágeis em organizações tradicionais, resultando em entregas 40% mais rápidas."
        ),
        (
            "Patricia Lima", "14/02/1991", "Data Science Professional Certificate, TensorFlow Developer, PyTorch Certified", 
            "Data Scientist", 
            "Especialista em machine learning e inteligência artificial com foco em soluções de NLP e visão computacional. Desenvolveu algoritmos de previsão de demanda que aumentaram a precisão em 35% comparado aos modelos anteriores."
        ),
        (
            "Marcelo Gomes", "30/10/1988", "Scrum Master Professional, Kanban Management Professional, SAFe Program Consultant", 
            "Agile Coach", 
            "Transformou a forma como equipes colaboram e entregam valor através da implementação de frameworks ágeis. Capacitou mais de 200 profissionais e auxiliou 15 equipes a melhorar sua velocidade de entrega em média 50%."
        ),
        (
            "Carla Mendes", "25/05/1983", "TOGAF Certified, AWS-Solutions Architect Professional, Azure-Solutions Architect Expert", 
            "Arquiteta Corporativa", 
            "Responsável por definir estratégias de arquitetura tecnológica alinhadas ao negócio. Liderou a migração completa de sistemas on-premise para cloud, resultando em economia anual de R$1,2 milhões em custos operacionais."
        ),
        (
            "Ricardo Ferreira", "11/08/1980", "Certified Ethical Hacker, Offensive Security Certified Professional, SANS GIAC Security Expert", 
            "Especialista em Segurança Ofensiva", 
            "Conduziu mais de 150 testes de penetração e avaliações de vulnerabilidade para sistemas críticos. Identificou e auxiliou na correção de falhas de segurança de alto impacto em aplicações que processam dados de milhões de usuários."
        ),
        (
            "Amanda Sousa", "02/01/1995", "Flutter Certified Developer, React Native Expert, AWS Mobile Developer", 
            "Desenvolvedora Mobile Senior", 
            "Especialista no desenvolvimento de aplicativos cross-platform de alta performance. Criou soluções móveis para o setor financeiro que atingiram mais de 3 milhões de downloads e mantiveram avaliação média de 4.8 estrelas."
        ),
        (
            "Paulo Vieira", "07/07/1987", "Kubernetes Application Developer, Docker Certified Associate, GCP-Professional Cloud Developer", 
            "Especialista em Containers e Microserviços", 
            "Arquiteto de infraestruturas baseadas em microserviços, com foco em escalabilidade e resiliência. Implementou arquiteturas que suportam picos de mais de 10.000 requisições por segundo com alta disponibilidade."
        )
    ]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.executemany('''
        INSERT INTO atendimentos (nome_funcionario, data_nascimento, certificacoes, especialidade, descricao)
        VALUES (?, ?, ?, ?, ?)
    ''', funcionarios)
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    create_database()
    insert_sample_data()
    print("Banco de dados e registros criados com sucesso!")