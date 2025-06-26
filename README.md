# Legislatech AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)

> Repositório oficial do [https://legisla.tech/ai](https://legisla.tech/ai)

## 📖 Sobre o Projeto

O **Legislatech AI** é uma plataforma de inteligência artificial especializada em análise e busca de legislação brasileira. Utilizando tecnologias avançadas de processamento de linguagem natural e machine learning, oferecemos soluções inteligentes para navegar, compreender e extrair insights da complexa legislação brasileira.

### 🎯 Objetivos

- **Democratizar o acesso** à legislação brasileira através de IA
- **Simplificar a busca** e compreensão de leis, decretos e regulamentações
- **Fornecer insights** inteligentes sobre relações entre diferentes normas
- **Automatizar análises** legais complexas

## 🏗️ Arquitetura

O projeto está organizado em módulos especializados:

```
legislatech-ai/
├── legislatech-ai-api/     # API REST com FastAPI
│   ├── routes/            # Endpoints da API
│   ├── utils/             # Utilitários e helpers
│   └── main.py            # Aplicação principal
└── README.md              # Este arquivo
```

## 🚀 Começando

### Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL com extensão pgvector
- Chave de API da OpenAI

### Instalação Rápida

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/legislatech-ai.git
   cd legislatech-ai
   ```

2. **Configure a API**
   ```bash
   cd legislatech-ai-api
   pip install -r requirements.txt
   # Configure as variáveis de ambiente
   uvicorn main:app --reload
   ```

3. **Acesse a documentação**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

Para instruções detalhadas, consulte o [README da API](legislatech-ai-api/README.md).

## 🔧 Tecnologias Utilizadas

- **Backend**: FastAPI, Python 3.10+
- **IA/ML**: LangChain, OpenAI GPT, RAG (Retrieval-Augmented Generation)
- **Banco de Dados**: PostgreSQL com pgvector
- **Processamento**: Rerankers, Embeddings, Vector Search
- **Deploy**: Docker, Uvicorn

## 📚 Funcionalidades Principais

### 🔍 Busca Inteligente
- **RAG Search**: Busca semântica com reranking automático
- **Intent Router**: Roteamento inteligente de consultas
- **Generic Search**: Busca flexível em múltiplos formatos

### 🕸️ Análise de Grafos
- **Grafo Crawler**: Navegação automática de relações legais
- **Análise de Conectividade**: Mapeamento de dependências entre normas
- **Visualização de Relacionamentos**: Identificação de impactos cruzados

### 🤖 Processamento de Linguagem Natural
- **Compreensão de Contexto**: Análise semântica de consultas
- **Extração de Informações**: Identificação automática de entidades legais
- **Geração de Respostas**: Respostas contextualizadas e precisas

## 🌐 API Endpoints

| Versão | Endpoint | Descrição |
|--------|----------|-----------|
| V1 | `/v1/search` | Busca com reranking |
| V2 | `/v2/intent` | Roteamento de intenções |
| V3 | `/v3/search` | Busca genérica |
| Grafo | `/grafo/crawl` | Navegação de grafos |

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [guia de contribuição](CONTRIBUTING.md) antes de submeter pull requests.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Website**: [https://legisla.tech/ai](https://legisla.tech/ai)
- **Email**: suporte@legisla.tech
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/legislatech-ai/issues)

## 🙏 Agradecimentos

- Comunidade open source
- Contribuidores e mantenedores
- Usuários que fornecem feedback valioso

---

**Desenvolvido com ❤️ pela equipe Legislatech**
