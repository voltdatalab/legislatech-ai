# Legislatech AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> **Repositório oficial do [https://legisla.tech/ai](https://legisla.tech/ai)** - Plataforma de IA para análise inteligente da legislação brasileira

## 📖 Sobre o Projeto

O **Legislatech AI** é uma plataforma de inteligência artificial especializada em análise e busca de legislação brasileira. Utilizando tecnologias avançadas de processamento de linguagem natural e machine learning, oferecemos soluções inteligentes para navegar, compreender e extrair insights da complexa legislação brasileira.

### 🎯 Objetivos

- **Democratizar o acesso** à legislação brasileira através de IA
- **Simplificar a busca** e compreensão de leis, decretos e regulamentações
- **Fornecer insights** inteligentes sobre relações entre diferentes normas
- **Automatizar análises** legais complexas
- **Reduzir tempo** de pesquisa jurídica em até 80%

### 🌟 Diferenciais

- **RAG Avançado**: Retrieval-Augmented Generation com reranking inteligente
- **Análise de Grafos**: Mapeamento automático de relações legais
- **Processamento em Português**: Otimizado para legislação brasileira
- **API RESTful**: Interface moderna e bem documentada
- **Escalabilidade**: Arquitetura preparada para alto volume

## 🏗️ Arquitetura

O projeto está organizado em módulos especializados com arquitetura moderna:

```
legislatech-ai/
├── legislatech-ai-api/     # API REST com FastAPI
│   ├── routes/            # Endpoints organizados por versão
│   │   ├── v1.py         # RAG Search com reranking
│   │   ├── v2.py         # Intent Router
│   │   ├── v3.py         # Generic Search
│   │   └── grafo.py      # Grafo Crawler
│   ├── utils/             # Utilitários e helpers
│   │   ├── auth.py       # Autenticação segura
│   │   ├── prompt_helpers.py # Helpers de prompts
│   │   └── sse.py        # Server-Sent Events
│   ├── config.py         # Configurações centralizadas
│   ├── main.py           # Aplicação principal
│   ├── intent_router.py  # Roteamento inteligente
│   ├── requirements.txt  # Dependências Python
│   ├── Dockerfile        # Containerização
│   └── README.md         # Documentação da API
└── README.md             # Este arquivo
```

## 🚀 Começando

### 📋 Pré-requisitos

- **Python 3.10+** (recomendado: 3.11)
- **PostgreSQL 13+** com extensão `pgvector`
- **Chave de API da OpenAI** (GPT-4 ou superior)
- **Docker** (opcional, para containerização)
- **Git** para clonagem do repositório

### ⚡ Instalação Rápida

#### Opção 1: Instalação Local

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/legislatech-ai.git
   cd legislatech-ai
   ```

2. **Configure a API**
   ```bash
   cd legislatech-ai-api
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate  # Windows
   
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env  # Se existir
   # Edite o arquivo .env com suas credenciais
   ```

4. **Execute a aplicação**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Opção 2: Com Docker

```bash
git clone https://github.com/seu-usuario/legislatech-ai.git
cd legislatech-ai/legislatech-ai-api
docker build -t legislatech-ai .
docker run -p 8000:8000 --env-file .env legislatech-ai
```

### 🔧 Configuração do Banco de Dados

1. **Instale o PostgreSQL e pgvector**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo apt-get install postgresql-13-pgvector  # Ajuste a versão
   
   # macOS
   brew install postgresql
   brew install pgvector
   ```

2. **Configure a extensão**
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   CREATE DATABASE legislatech;
   ```

3. **Configure a string de conexão**
   ```env
   POSTGRES_CONNECTION_STRING=postgresql://usuario:senha@localhost:5432/legislatech
   ```

### 📚 Documentação Interativa

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Tecnologias Utilizadas

### 🐍 Backend
- **FastAPI 0.115+**: Framework web moderno e rápido
- **Python 3.10+**: Linguagem principal
- **Uvicorn**: Servidor ASGI de alta performance
- **Pydantic**: Validação de dados e serialização

### 🤖 IA/ML
- **LangChain 0.3+**: Framework para aplicações de IA
- **OpenAI GPT-4**: Modelo de linguagem avançado
- **RAG (Retrieval-Augmented Generation)**: Busca semântica
- **Embeddings**: Text-embedding-3-large
- **Rerankers**: FlashRank para otimização de resultados

### 🗄️ Banco de Dados
- **PostgreSQL 13+**: Banco relacional robusto
- **pgvector**: Extensão para busca vetorial
- **SQLAlchemy**: ORM e pool de conexões
- **AsyncPG**: Driver assíncrono

### 🐳 DevOps
- **Docker**: Containerização
- **Environment Variables**: Configuração segura
- **Git**: Controle de versão

## 📚 Funcionalidades Principais

### 🔍 Busca Inteligente

#### RAG Search (V1)
- **Busca semântica** com embeddings avançados
- **Reranking automático** para relevância
- **Contexto inteligente** para respostas precisas
- **Cache otimizado** para performance

```bash
curl -X POST "http://localhost:8000/v1/responses" \
     -H "Authorization: Basic $(echo -n 'usuario:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{"input": [{"role": "user", "content": [{"type": "text", "text": "Quais são os direitos do trabalhador em caso de acidente de trabalho?"}]}]}'
```

#### Intent Router (V2)
- **Classificação automática** de intenções
- **Roteamento inteligente** para endpoints específicos
- **Análise de contexto** para melhor direcionamento

#### Generic Search (V3)
- **Busca flexível** em múltiplos formatos
- **Filtros avançados** por metadados
- **Streaming de resultados** em tempo real

### 🕸️ Análise de Grafos

#### Grafo Crawler
- **Navegação automática** de relações legais
- **Mapeamento de dependências** entre normas
- **Análise de impacto** cruzado
- **Visualização de relacionamentos**

```bash
curl -X GET "http://localhost:8000/grafo/" \
     -H "Authorization: Basic $(echo -n 'usuario:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{
       "urls": "https://www.planalto.gov.br/ccivil_03/leis/l8078.htm",
       "profundidade": 2,
       "top_n": 20
     }'
```

### 🤖 Processamento de Linguagem Natural

#### Compreensão de Contexto
- **Análise semântica** de consultas em português
- **Extração de entidades** legais
- **Classificação de documentos** por tipo

#### Geração de Respostas
- **Respostas contextualizadas** e precisas
- **Citações automáticas** de fontes
- **Formatação estruturada** de resultados

## 🌐 API Endpoints

| Versão | Endpoint | Método | Descrição | Autenticação |
|--------|----------|--------|-----------|--------------|
| V1 | `/v1/responses` | POST | Busca com reranking e streaming | ✅ |
| V2 | `/v2/responses` | POST | Busca híbrida com queries expandidas | ✅ |
| V3 | `/v3/responses` | POST | Busca genérica simples | ✅ |
| Grafo | `/grafo/` | GET | Navegação de grafos com PageRank | ❌ |
| Root | `/` | GET | Health check e informações da API | ❌ |

### 🔐 Autenticação

A API utiliza autenticação HTTP Basic para endpoints sensíveis:

```bash
curl -X POST "http://localhost:8000/v1/responses" \
     -H "Authorization: Basic $(echo -n 'usuario:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{"input": [{"role": "user", "content": [{"type": "text", "text": "teste"}]}]}'
```

## 🧪 Exemplos de Uso

### Busca de Legislação Trabalhista

```python
import requests
import base64

# Busca sobre direitos trabalhistas
response = requests.post("http://localhost:8000/v1/responses", 
    headers={
        "Authorization": "Basic " + base64.b64encode(b"admin:senha").decode(),
        "Content-Type": "application/json"
    },
    json={
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Quais são os direitos do trabalhador em caso de acidente de trabalho?"
                    }
                ]
            }
        ]
    }
)

print(response.text)  # Resposta em formato SSE
```

### Análise de Relacionamentos Legais

```python
# Análise de grafo de uma lei específica
response = requests.get("http://localhost:8000/grafo/", params={
    "urls": "https://www.planalto.gov.br/ccivil_03/leis/l8078.htm",
    "profundidade": 2,
    "top_n": 20
})

print(response.json())
```

## 📊 Performance e Escalabilidade

### Métricas Esperadas
- **Latência**: < 500ms para buscas simples
- **Throughput**: 100+ requisições/segundo
- **Precisão**: > 85% em buscas semânticas
- **Disponibilidade**: 99.9% uptime

### Otimizações Implementadas
- **Cache Redis** para resultados frequentes
- **Pool de conexões** otimizado
- **Indexação vetorial** para busca rápida
- **Streaming** para respostas longas

## 🚀 Deploy em Produção

### Variáveis de Ambiente Necessárias

```env
# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Database
POSTGRES_CONNECTION_STRING=postgresql://user:pass@host:5432/db

# Authentication
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=secure-password

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: ./legislatech-ai-api
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_CONNECTION_STRING=postgresql://user:pass@db:5432/legislatech
    depends_on:
      - db
  
  db:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: legislatech
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Este projeto é mantido pela comunidade.

### Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit suas mudanças** (`git commit -m 'Add some AmazingFeature'`)
4. **Push para a branch** (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

### Diretrizes de Contribuição

- **Código limpo**: Siga PEP 8 e use type hints
- **Testes**: Adicione testes para novas funcionalidades
- **Documentação**: Atualize docs quando necessário
- **Commits**: Use mensagens descritivas

### Áreas para Contribuição

- 🐛 **Bug fixes** e melhorias
- ✨ **Novas funcionalidades**
- 📚 **Melhorias na documentação**
- 🧪 **Testes e cobertura**
- 🚀 **Otimizações de performance**

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

A Licença MIT permite:
- ✅ Uso comercial
- ✅ Modificação
- ✅ Distribuição
- ✅ Uso privado
- ❌ Responsabilidade do autor

## 🆘 Suporte e Comunidade

### Canais de Suporte

- **Website**: [https://legisla.tech/ai](https://legisla.tech/ai)
- **Email**: suporte@legisla.tech
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/legislatech-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/seu-usuario/legislatech-ai/discussions)

### FAQ

**Q: Como configurar o pgvector?**
A: Veja a seção "Configuração do Banco de Dados" acima.

**Q: Qual versão do Python é suportada?**
A: Python 3.10 ou superior (recomendado 3.11).

**Q: Como obter uma chave da OpenAI?**
A: Acesse [platform.openai.com](https://platform.openai.com) e crie uma conta.

## 🙏 Agradecimentos

- **Comunidade open source** que torna projetos como este possíveis
- **Contribuidores** que dedicam tempo e expertise
- **Usuários** que fornecem feedback valioso
- **Equipe Legislatech** pelo desenvolvimento contínuo

## 📈 Roadmap

### Próximas Versões

- [ ] **v2.0**: Interface web completa
- [ ] **v2.1**: Análise de sentimento em decisões judiciais
- [ ] **v2.2**: Integração com sistemas jurídicos
- [ ] **v3.0**: IA multimodal (texto + imagens)

### Funcionalidades Planejadas

- 🔮 **Análise preditiva** de tendências legais
- 🎯 **Recomendações personalizadas** por área do direito
- 📊 **Dashboards analíticos** para advogados
- 🤖 **Chatbot especializado** em legislação

---

**Desenvolvido com ❤️ pela equipe Legislatech**

*Transformando a forma como interagimos com a legislação brasileira através da inteligência artificial.*
