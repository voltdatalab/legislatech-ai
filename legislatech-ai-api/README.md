# Legislatech AI API

API de inteligência artificial para busca e análise de legislação brasileira, desenvolvida com FastAPI e LangChain.

## 🚀 Funcionalidades

- **RAG Search**: Busca semântica com reranking
- **Intent Router**: Roteamento inteligente de intenções
- **Generic Search**: Busca genérica em documentos
- **Grafo Crawler**: Navegação e análise de grafos de legislação

## 📋 Pré-requisitos

- Python 3.10+
- PostgreSQL com extensão pgvector
- Variáveis de ambiente configuradas

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/legislatech-ai.git
cd legislatech-ai/legislatech-ai-api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do banco de dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/legislatech

# Configurações da OpenAI
OPENAI_API_KEY=sua_chave_api_aqui

# Outras configurações
ENVIRONMENT=development
```

### 5. Configure o banco de dados
Certifique-se de que o PostgreSQL está rodando e que a extensão `pgvector` está instalada:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 🚀 Executando a aplicação

### Desenvolvimento
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Com Docker
```bash
docker build -t legislatech-ai-api .
docker run -p 8000:8000 legislatech-ai-api
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints Disponíveis

### V1 - Rerank Search
- `POST /v1/search` - Busca com reranking

### V2 - Intent Router
- `POST /v2/intent` - Roteamento de intenções

### V3 - Generic Search
- `POST /v3/search` - Busca genérica

### Grafo Crawler
- `POST /grafo/crawl` - Navegação de grafos

## 🧪 Testando a API

### Exemplo de busca RAG
```bash
curl -X POST "http://localhost:8000/v1/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Qual é a legislação sobre proteção de dados?",
       "limit": 5
     }'
```

## 📁 Estrutura do Projeto

```
legislatech-ai-api/
├── main.py              # Aplicação principal FastAPI
├── config.py            # Configurações
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── routes/             # Módulos de rotas
│   ├── v1.py          # Endpoints V1
│   ├── v2.py          # Endpoints V2
│   ├── v3.py          # Endpoints V3
│   └── grafo.py       # Endpoints do grafo
└── utils/              # Utilitários
    ├── auth.py         # Autenticação
    ├── prompt_helpers.py # Helpers de prompts
    └── sse.py          # Server-Sent Events
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 🆘 Suporte

Para suporte, envie um email para suporte@legisla.tech ou abra uma issue no GitHub.
