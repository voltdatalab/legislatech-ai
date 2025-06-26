# Legislatech AI API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> **API de inteligência artificial para busca e análise de legislação brasileira** - Desenvolvida com FastAPI e LangChain

## 🚀 Funcionalidades

### 🔍 Busca Inteligente
- **RAG Search**: Busca semântica com reranking automático
- **Intent Router**: Roteamento inteligente de intenções
- **Generic Search**: Busca genérica em documentos
- **Grafo Crawler**: Navegação e análise de grafos de legislação

### 🤖 Processamento Avançado
- **Embeddings**: Text-embedding-3-large para representação vetorial
- **Reranking**: FlashRank para otimização de relevância
- **Tokenização**: Tiktoken para contagem precisa de tokens
- **Streaming**: Respostas em tempo real via Server-Sent Events

### 🔐 Segurança
- **Autenticação HTTP Basic** para endpoints sensíveis
- **Validação de entrada** com Pydantic
- **Sanitização de dados** automática
- **Rate limiting** configurável

## 📋 Pré-requisitos

### Sistema
- **Python 3.10+** (recomendado: 3.11)
- **PostgreSQL 13+** com extensão pgvector
- **8GB RAM** mínimo (16GB recomendado)
- **2GB** espaço em disco

### Dependências Externas
- **Chave de API da OpenAI** (GPT-4 ou superior)
- **Acesso à internet** para embeddings e LLMs
- **Git** para clonagem

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/legislatech-ai.git
cd legislatech-ai/legislatech-ai-api
```

### 2. Crie um ambiente virtual
```bash
# Python venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Alternativa: Conda
conda create -n legislatech python=3.11
conda activate legislatech
```

### 3. Instale as dependências
```bash
# Atualize pip
pip install --upgrade pip

# Instale dependências
pip install -r requirements.txt

# Para desenvolvimento (opcional)
pip install -r requirements-dev.txt  # Se existir
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# === Configurações da OpenAI ===
OPENAI_API_KEY=sk-your-openai-api-key-here

# === Configurações do Banco de Dados ===
POSTGRES_CONNECTION_STRING=postgresql://usuario:senha@localhost:5432/legislatech

# === Autenticação ===
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=senha-segura-aqui

# === Configurações da Aplicação ===
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# === Configurações de Performance ===
MAX_TOKENS=4000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# === Configurações de Cache ===
CACHE_TTL=3600
CACHE_MAX_SIZE=1000
```

### 5. Configure o banco de dados

#### Instalação do PostgreSQL + pgvector

**Ubuntu/Debian:**
```bash
# Instale PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Instale pgvector
sudo apt install postgresql-13-pgvector  # Ajuste a versão

# Inicie o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
# Com Homebrew
brew install postgresql
brew install pgvector

# Inicie o serviço
brew services start postgresql
```

**Docker:**
```bash
docker run -d \
  --name postgres-legislatech \
  -e POSTGRES_DB=legislatech \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=senha \
  -p 5432:5432 \
  pgvector/pgvector:pg15
```

#### Configuração do Banco
```sql
-- Conecte ao PostgreSQL
sudo -u postgres psql

-- Crie o banco e usuário
CREATE DATABASE legislatech;
CREATE USER usuario WITH PASSWORD 'senha';
GRANT ALL PRIVILEGES ON DATABASE legislatech TO usuario;

-- Conecte ao banco legislatech
\c legislatech

-- Instale a extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Crie índices otimizados (opcional)
CREATE INDEX IF NOT EXISTS idx_document_embedding ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### 6. Verifique a instalação
```bash
# Teste a conexão com o banco
python -c "
from config import engine
try:
    with engine.connect() as conn:
        result = conn.execute('SELECT version()')
        print('✅ Conexão com PostgreSQL OK:', result.fetchone()[0])
except Exception as e:
    print('❌ Erro na conexão:', e)
"

# Teste a API da OpenAI
python -c "
import os
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
try:
    response = openai.models.list()
    print('✅ Conexão com OpenAI OK')
except Exception as e:
    print('❌ Erro na OpenAI:', e)
"
```

## 🚀 Executando a aplicação

### Desenvolvimento
```bash
# Com reload automático
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

# Com workers múltiplos
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Com configurações customizadas
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --access-log --log-config log_config.json
```

### Produção
```bash
# Com Gunicorn (recomendado)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Com Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Com Docker
```bash
# Build da imagem
docker build -t legislatech-ai-api .

# Execução
docker run -p 8000:8000 --env-file .env legislatech-ai-api

# Com volumes para desenvolvimento
docker run -p 8000:8000 --env-file .env -v $(pwd):/app legislatech-ai-api

# Com Docker Compose
docker-compose up -d
```

## 📚 Documentação da API

### Endpoints Interativos
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Health Check
```bash
curl http://localhost:8000/health
```

## 🔗 Endpoints Disponíveis

### V1 - Rerank Search
| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/v1/search` | POST | Busca com reranking | ✅ |
| `/v1/responses` | POST | Respostas streaming | ✅ |

**Exemplo de busca:**
```bash
curl -X POST "http://localhost:8000/v1/search" \
     -H "Authorization: Basic $(echo -n 'admin:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Quais são os direitos trabalhistas em caso de demissão?",
       "limit": 5,
       "rerank": true,
       "filters": {
         "tipo": "lei",
         "ano": "2023"
       }
     }'
```

### V2 - Intent Router
| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/v2/intent` | POST | Roteamento de intenções | ❌ |
| `/v2/responses` | POST | Respostas streaming | ✅ |

**Exemplo de roteamento:**
```bash
curl -X POST "http://localhost:8000/v2/intent" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Preciso saber sobre férias trabalhistas",
       "context": "advogado trabalhista"
     }'
```

### V3 - Generic Search
| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/v3/search` | POST | Busca genérica | ❌ |
| `/v3/responses` | POST | Respostas streaming | ✅ |

### Grafo Crawler
| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/grafo/crawl` | POST | Navegação de grafos | ❌ |

**Exemplo de crawling:**
```bash
curl -X POST "http://localhost:8000/grafo/crawl" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://www.planalto.gov.br/ccivil_03/leis/l8078.htm",
       "depth": 3,
       "max_pages": 50,
       "filters": {
         "tipo": ["lei", "decreto"],
         "ano_min": 2020
       }
     }'
```

## 🧪 Testando a API

### Testes Automatizados
```bash
# Instale pytest
pip install pytest pytest-asyncio httpx

# Execute os testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=. --cov-report=html
```

### Testes Manuais

#### 1. Teste de Conectividade
```bash
# Health check
curl http://localhost:8000/

# Status da API
curl http://localhost:8000/health
```

#### 2. Teste de Autenticação
```bash
# Sem autenticação (deve falhar)
curl -X POST "http://localhost:8000/v1/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "teste"}'

# Com autenticação (deve funcionar)
curl -X POST "http://localhost:8000/v1/search" \
     -H "Authorization: Basic $(echo -n 'admin:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{"query": "teste"}'
```

#### 3. Teste de Busca RAG
```bash
curl -X POST "http://localhost:8000/v1/search" \
     -H "Authorization: Basic $(echo -n 'admin:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Qual é a legislação sobre proteção de dados?",
       "limit": 3,
       "rerank": true
     }'
```

#### 4. Teste de Streaming
```bash
curl -X POST "http://localhost:8000/v1/responses" \
     -H "Authorization: Basic $(echo -n 'admin:senha' | base64)" \
     -H "Content-Type: application/json" \
     -d '{
       "input": [
         {
           "role": "user",
           "content": [
             {
               "type": "text",
               "text": "Explique o Código de Defesa do Consumidor"
             }
           ]
         }
       ]
     }' \
     --no-buffer
```

## 📁 Estrutura do Projeto

```
legislatech-ai-api/
├── main.py              # Aplicação principal FastAPI
├── config.py            # Configurações centralizadas
├── intent_router.py     # Roteamento inteligente
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── captain-definition  # Configuração CapRover
├── routes/             # Módulos de rotas
│   ├── __init__.py
│   ├── v1.py          # Endpoints V1 - RAG Search
│   ├── v2.py          # Endpoints V2 - Intent Router
│   ├── v3.py          # Endpoints V3 - Generic Search
│   └── grafo.py       # Endpoints do grafo
└── utils/              # Utilitários
    ├── __init__.py
    ├── auth.py         # Autenticação HTTP Basic
    ├── prompt_helpers.py # Helpers de prompts e tokens
    └── sse.py          # Server-Sent Events
```

### Descrição dos Módulos

#### `main.py`
- Configuração da aplicação FastAPI
- Middleware CORS
- Registro de rotas
- Endpoint de health check

#### `config.py`
- Carregamento de variáveis de ambiente
- Configuração de conexões com banco
- Instâncias globais (embeddings, vector store)
- Configurações de performance

#### `routes/`
- **v1.py**: Implementação RAG com reranking
- **v2.py**: Sistema de roteamento de intenções
- **v3.py**: Busca genérica flexível
- **grafo.py**: Crawler e análise de grafos

#### `utils/`
- **auth.py**: Autenticação HTTP Basic segura
- **prompt_helpers.py**: Gerenciamento de tokens e prompts
- **sse.py**: Streaming de respostas

## 🔧 Configurações Avançadas

### Performance

#### Otimizações de Banco
```sql
-- Índices para busca vetorial
CREATE INDEX CONCURRENTLY idx_documents_embedding 
ON documents USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Índices para metadados
CREATE INDEX CONCURRENTLY idx_documents_metadata 
ON documents USING gin (metadata);

-- Índices para busca textual
CREATE INDEX CONCURRENTLY idx_documents_content 
ON documents USING gin(to_tsvector('portuguese', content));
```

#### Configurações de Pool
```python
# Em config.py
engine = create_engine(
    CONNECTION_STRING,
    pool_size=20,           # Aumente para produção
    max_overflow=30,        # Mais conexões sob demanda
    pool_pre_ping=True,     # Verifica conexões
    pool_recycle=3600,      # Recicla conexões a cada hora
    echo=False              # Logs SQL (False em produção)
)
```

### Cache

#### Redis (Recomendado)
```bash
# Instale Redis
sudo apt install redis-server  # Ubuntu
brew install redis            # macOS

# Configure no .env
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600
```

#### Cache em Memória
```python
from functools import lru_cache
import time

@lru_cache(maxsize=1000)
def cached_search(query: str, limit: int = 5):
    # Implementação com cache
    pass
```

### Logging

#### Configuração Avançada
```python
import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "logs/app.log"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO"
        }
    }
}

dictConfig(logging_config)
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com PostgreSQL
```bash
# Verifique se o PostgreSQL está rodando
sudo systemctl status postgresql

# Verifique a string de conexão
echo $POSTGRES_CONNECTION_STRING

# Teste a conexão manualmente
psql $POSTGRES_CONNECTION_STRING -c "SELECT version();"
```

#### 2. Erro de API Key da OpenAI
```bash
# Verifique se a chave está definida
echo $OPENAI_API_KEY

# Teste a chave
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

#### 3. Erro de pgvector
```sql
-- Verifique se a extensão está instalada
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Instale se necessário
CREATE EXTENSION IF NOT EXISTS vector;
```

#### 4. Erro de Memória
```bash
# Aumente a memória do Python
export PYTHONMALLOC=malloc
export PYTHONDEVMODE=1

# Ou use swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 5. Erro de Dependências
```bash
# Limpe o cache do pip
pip cache purge

# Reinstale as dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --no-cache-dir
```

### Logs Úteis

#### Verificar Logs da Aplicação
```bash
# Logs do Uvicorn
uvicorn main:app --log-level debug

# Logs do sistema
journalctl -u legislatech-api -f

# Logs do Docker
docker logs legislatech-api -f
```

#### Monitoramento de Performance
```bash
# Uso de CPU e memória
htop

# Conexões de banco
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Logs de queries lentas
tail -f /var/log/postgresql/postgresql-*.log | grep "duration:"
```

## 🚀 Deploy em Produção

### Docker Compose Completo
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_CONNECTION_STRING=postgresql://user:pass@db:5432/legislatech
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - BASIC_AUTH_USERNAME=${BASIC_AUTH_USERNAME}
      - BASIC_AUTH_PASSWORD=${BASIC_AUTH_PASSWORD}
      - ENVIRONMENT=production
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: legislatech
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d legislatech"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

### Nginx Configuration
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name api.legisla.tech;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Systemd Service
```ini
[Unit]
Description=Legislatech AI API
After=network.target

[Service]
Type=exec
User=legislatech
WorkingDirectory=/opt/legislatech-ai-api
Environment=PATH=/opt/legislatech-ai-api/venv/bin
ExecStart=/opt/legislatech-ai-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 🤝 Contribuindo

### Setup de Desenvolvimento
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/legislatech-ai.git
cd legislatech-ai/legislatech-ai-api

# Configure o ambiente
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Instale pre-commit hooks
pip install pre-commit
pre-commit install

# Configure o banco de teste
createdb legislatech_test
```

### Diretrizes de Código
- **PEP 8**: Siga o estilo de código Python
- **Type Hints**: Use sempre que possível
- **Docstrings**: Documente funções e classes
- **Testes**: Mantenha cobertura > 80%

### Fluxo de Trabalho
1. **Crie uma branch** para sua feature
2. **Desenvolva** com testes
3. **Execute linting** e testes
4. **Faça commit** com mensagem descritiva
5. **Abra Pull Request**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 🆘 Suporte

### Canais de Ajuda
- **Documentação**: [docs.legisla.tech](https://docs.legisla.tech)
- **Email**: suporte@legisla.tech
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/legislatech-ai/issues)
- **Discord**: [Comunidade Legislatech](https://discord.gg/legislatech)

### FAQ

**Q: Como aumentar a performance da busca?**
A: Configure índices vetoriais, use cache Redis e ajuste o pool de conexões.

**Q: Como debugar problemas de embedding?**
A: Verifique a chave da OpenAI e use logs de debug.

**Q: Como escalar horizontalmente?**
A: Use load balancer, múltiplas instâncias e banco de dados replicado.

---

**Desenvolvido com ❤️ pela equipe Legislatech**

*Transformando a pesquisa jurídica através da inteligência artificial.*
