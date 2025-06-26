# Legislatech AI Crawlers

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)](https://playwright.dev/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![Spacy](https://img.shields.io/badge/Spacy-NLP-purple.svg)](https://spacy.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> **Sistema de crawlers especializados para coleta automatizada de legislação brasileira** - Desenvolvido com Playwright, BeautifulSoup e IA

## 🚀 Sobre o Projeto

O **Legislatech AI Crawlers** é um sistema modular de web scraping especializado na coleta automatizada de legislação brasileira. Utilizando tecnologias avançadas de automação web e processamento de linguagem natural, extraímos, processamos e estruturamos dados legislativos de fontes oficiais.

### 🎯 Objetivos

- **Automatizar a coleta** de legislação de fontes oficiais
- **Estruturar dados** legislativos de forma consistente
- **Processar metadados** com IA (datas, nomes, entidades)
- **Manter histórico** completo de alterações legislativas
- **Garantir qualidade** dos dados coletados

### 🌟 Diferenciais

- **Automação Inteligente**: Playwright para sites dinâmicos
- **Processamento de IA**: Reconhecimento de nomes e datas
- **Modularidade**: Crawlers especializados por tipo de legislação
- **Robustez**: Tratamento de erros e retry automático
- **Escalabilidade**: Processamento paralelo com workers

## 📋 Tipos de Legislação Suportados

### 📜 Legislação Federal
- **Leis Ordinárias**: Leis comuns do Congresso Nacional
- **Leis Complementares**: Leis que complementam a Constituição
- **Leis Delegadas**: Leis delegadas pelo Congresso ao Presidente
- **Medidas Provisórias**: MPs editadas pelo Presidente
- **Decretos**: Atos normativos do Presidente
- **Emendas Constitucionais**: Modificações na Constituição

### 🏛️ Órgãos Específicos
- **ANTT**: Agência Nacional de Transportes Terrestres
- **BCB**: Banco Central do Brasil
- **ANA**: Agência Nacional de Águas

### 📚 Códigos e Estatutos
- **Código de Defesa do Consumidor**: Lei 8.078/1990
- **Histórico de Códigos**: Evolução dos códigos brasileiros
- **Histórico de Constituições**: Constituições históricas
- **Estatutos**: Estatutos específicos

### 📄 Documentos Especiais
- **Mensagens de Veto**: Veto total ou parcial do Presidente
- **Resoluções ANA**: Resoluções da Agência Nacional de Águas
- **Legislação e Publicação**: Documentos de publicação oficial

## 🏗️ Arquitetura

### Visão Geral do Sistema Legislatech AI

O **Legislatech AI** é um ecossistema completo de inteligência artificial para análise de legislação brasileira, composto por três módulos principais:

```
legislatech-ai/
├── legislatech-ai-api/           # API REST com FastAPI
│   ├── routes/                  # Endpoints organizados por versão
│   │   ├── v1.py               # RAG Search com reranking
│   │   ├── v2.py               # Intent Router
│   │   ├── v3.py               # Generic Search
│   │   └── grafo.py            # Grafo Crawler
│   ├── utils/                   # Utilitários e helpers
│   │   ├── auth.py             # Autenticação segura
│   │   ├── prompt_helpers.py   # Helpers de prompts
│   │   └── sse.py              # Server-Sent Events
│   ├── config.py               # Configurações centralizadas
│   ├── main.py                 # Aplicação principal
│   ├── intent_router.py        # Roteamento inteligente
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile             # Containerização
│   └── README.md              # Documentação da API
├── legislatech-ai-crawlers/     # Sistema de Crawlers
│   ├── leis-ordinarias/        # Crawler de Leis Ordinárias
│   ├── decretos-emendas/       # Crawler de Decretos e Emendas
│   ├── medidas-provisorias/    # Crawler de Medidas Provisórias
│   ├── antt/                   # Crawler da ANTT
│   ├── bcb/                    # Crawler do BCB
│   ├── codigo-consumidor/      # Crawler do CDC
│   ├── historico-codigos/      # Crawler de códigos históricos
│   ├── historico-constituicoes/ # Crawler de constituições
│   ├── historico-decretos/     # Crawler de decretos históricos
│   ├── historico-decretos-leis/ # Crawler de decretos-leis
│   ├── historico-estatutos/    # Crawler de estatutos
│   ├── legislacao-e-publicacao/ # Crawler de publicações
│   ├── leis-complementares/    # Crawler de leis complementares
│   ├── leis-delegadas/         # Crawler de leis delegadas
│   ├── resolucoes-ana/         # Crawler de resoluções ANA
│   ├── mensagem-de-veto-total/ # Crawler de vetos
│   ├── requirements.txt        # Dependências globais
│   └── README.md              # Este arquivo
└── README.md                   # Documentação principal
```

### Arquitetura dos Crawlers

Cada crawler segue uma estrutura modular padronizada:

```
crawler-especifico/
├── main.py              # Lógica principal do crawler
├── agents.py            # Agentes de IA para processamento
├── date_spacy/          # Pipeline de reconhecimento de datas
├── dicionario_dados     # Estrutura de dados
├── requirements.txt     # Dependências específicas
├── Dockerfile          # Containerização
└── .env                # Configurações de ambiente
```

### Fluxo de Dados

```
1. Fontes Oficiais
   ↓
2. Crawlers Especializados
   ├── Playwright (automação web)
   ├── BeautifulSoup (parsing HTML)
   └── Cloudscraper (bypass anti-bot)
   ↓
3. Processamento com IA
   ├── Reconhecimento de nomes (GPT-4)
   ├── Extração de datas (Spacy customizado)
   └── Sanitização de texto
   ↓
4. Estruturação de Dados
   ├── Metadados padronizados
   ├── Texto processado
   └── Relacionamentos
   ↓
5. Armazenamento
   ├── PostgreSQL + pgvector
   ├── Embeddings vetoriais
   └── Índices otimizados
   ↓
6. API de Consulta
   ├── RAG Search
   ├── Intent Router
   └── Generic Search
```

### Tecnologias por Camada

#### 🕷️ **Camada de Coleta**
- **Playwright**: Automação de navegadores para sites dinâmicos
- **BeautifulSoup**: Parsing HTML e extração de conteúdo
- **Cloudscraper**: Bypass de proteções anti-bot
- **Requests**: Requisições HTTP assíncronas

#### 🤖 **Camada de IA**
- **OpenAI GPT-4**: Reconhecimento de nomes e entidades
- **Spacy**: Processamento de linguagem natural
- **Pipeline Customizado**: Reconhecimento de datas em português
- **Agentes Especializados**: Validação e classificação

#### 🗄️ **Camada de Dados**
- **PostgreSQL**: Banco de dados principal
- **pgvector**: Extensão para busca vetorial
- **SQLAlchemy**: ORM e pool de conexões
- **Pandas**: Manipulação e análise de dados

#### 🔧 **Camada de Processamento**
- **ThreadPoolExecutor**: Processamento paralelo
- **Retry Logic**: Tratamento de falhas
- **Rate Limiting**: Controle de requisições
- **Logging**: Monitoramento detalhado

### Integração com a API

Os crawlers alimentam a API através de:

1. **Coleta Contínua**: Dados atualizados regularmente
2. **Estrutura Padronizada**: Formato consistente para todos os tipos
3. **Metadados Enriquecidos**: Informações processadas com IA
4. **Relacionamentos**: Conexões entre documentos legais

### Escalabilidade

#### Horizontal
- **Crawlers Independentes**: Cada tipo de legislação em container separado
- **Workers Paralelos**: Processamento simultâneo de múltiplos documentos
- **Load Balancing**: Distribuição de carga entre instâncias

#### Vertical
- **Otimização de Memória**: Gerenciamento eficiente de recursos
- **Cache Inteligente**: Redução de requisições desnecessárias
- **Compressão de Dados**: Armazenamento otimizado

### Monitoramento e Observabilidade

#### Métricas Coletadas
- **Taxa de Sucesso**: % de páginas coletadas com sucesso
- **Tempo de Processamento**: Latência por documento
- **Uso de Recursos**: CPU, memória, rede
- **Qualidade dos Dados**: Precisão das extrações

#### Logs Estruturados
- **Nível de Aplicação**: Operações dos crawlers
- **Nível de Sistema**: Recursos e performance
- **Nível de Negócio**: Dados coletados e processados

### Segurança

#### Proteções Implementadas
- **Rate Limiting**: Controle de velocidade de requisições
- **User-Agent Rotation**: Variação de identificadores
- **Proxy Support**: Suporte a proxies para anonimização
- **Error Handling**: Tratamento seguro de falhas

#### Boas Práticas
- **Respeito aos robots.txt**: Conformidade com diretrizes dos sites
- **Delays Inteligentes**: Pausas entre requisições
- **Retry com Backoff**: Tentativas com intervalos crescentes
- **Sanitização de Dados**: Limpeza de conteúdo malicioso

## 🛠️ Pré-requisitos

### Sistema
- **Python 3.12+** (recomendado)
- **8GB RAM** mínimo (16GB recomendado)
- **Conexão estável** com a internet
- **Docker** (opcional, para containerização)

### Dependências Externas
- **Chave de API da OpenAI** (GPT-4 ou superior)
- **Acesso aos sites** oficiais do governo
- **Git** para clonagem

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/legislatech-ai.git
cd legislatech-ai/legislatech-ai-crawlers
```

### 2. Configure o ambiente
```bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instale dependências globais
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` em cada crawler:

```env
# === Configurações da OpenAI ===
OPENAI_API_KEY=sk-your-openai-api-key-here

# === Configurações do Banco de Dados ===
DATABASE_URL=postgresql://usuario:senha@localhost:5432/legislatech

# === Configurações do Crawler ===
WORKERS=10
TIMEOUT=60
RETRY_ATTEMPTS=3
DELAY_BETWEEN_REQUESTS=1

# === Configurações de Log ===
LOG_LEVEL=INFO
SAVE_RAW_DATA=true
```

### 4. Instale o Playwright
```bash
# Instale os navegadores necessários
playwright install

# Ou instale apenas o Chromium
playwright install chromium
```

### 5. Configure o Spacy (se necessário)
```bash
# Baixe o modelo português (se usar)
python -m spacy download pt_core_news_sm

# Ou use o modelo customizado (já incluído)
# Os modelos customizados estão em date_spacy/
```

## 🔧 Executando os Crawlers

### Execução Individual

#### Leis Ordinárias
```bash
cd leis-ordinarias
python main.py
```

#### Decretos e Emendas
```bash
cd decretos-emendas
python main.py
```

#### Medidas Provisórias
```bash
cd medidas-provisorias
python main.py
```

### Execução com Docker

#### Build da imagem
```bash
cd leis-ordinarias
docker build -t legislatech-crawler-leis .
```

#### Execução
```bash
docker run --env-file .env legislatech-crawler-leis
```

### Execução Paralela
```bash
# Execute múltiplos crawlers simultaneamente
python -c "
import subprocess
import threading

crawlers = [
    'leis-ordinarias',
    'decretos-emendas', 
    'medidas-provisorias'
]

def run_crawler(crawler):
    subprocess.run(['python', 'main.py'], cwd=crawler)

threads = []
for crawler in crawlers:
    t = threading.Thread(target=run_crawler, args=(crawler,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
"
```

## 📊 Estrutura de Dados

### Formato Padrão dos Dados

```python
{
    # === Metadados Básicos ===
    'num_lei': '12345',                    # Número da lei
    'data_lei': '2023-12-01',              # Data da lei
    'data_dou': '2023-12-02',              # Data publicação DOU
    'ano': 2023,                           # Ano da legislação
    
    # === Texto Processado ===
    'bleached_nome': 'Lei 12345 de 2023',  # Nome limpo
    'non_bleached_nome': 'Lei nº 12.345, de 1º de dezembro de 2023',  # Nome original
    'ementa': 'Dispõe sobre...',           # Ementa da lei
    
    # === Conteúdo Completo ===
    'lei_text': 'Texto da lei processado...',           # Texto limpo
    'non_parsed_lei_text': 'Texto original...',         # Texto original
    'lei_text_striked': 'Texto revogado...',            # Texto revogado
    'full_lei_text': 'Texto completo...',               # Texto completo
    
    # === Metadados Avançados ===
    'sancionadores': ['João Silva', 'Maria Santos'],     # Nomes extraídos
    'link': 'https://www.planalto.gov.br/...',          # URL original
    'crawled_at': '2023-12-01T10:00:00Z'                # Timestamp
}
```

### Campos Específicos por Tipo

#### Leis Ordinárias
- `num_lei`: Número da lei
- `data_lei`: Data de sanção
- `data_dou`: Data de publicação no DOU

#### Medidas Provisórias
- `num_mp`: Número da MP
- `data_edicao`: Data de edição
- `data_aprovacao`: Data de aprovação pelo Congresso

#### Decretos
- `num_decreto`: Número do decreto
- `data_decreto`: Data do decreto
- `tipo_decreto`: Tipo (executivo, legislativo, etc.)

## 🤖 Processamento com IA

### Reconhecimento de Nomes

O sistema utiliza agentes de IA para extrair e validar nomes de pessoas:

```python
from agents import run_name_recognizer_agent

# Lista de possíveis nomes extraídos do texto
possible_names = ['João da Silva', 'Casa de papel', 'Carlos Alberto']

# Validação com IA
valid_names = run_name_recognizer_agent(
    list_of_names=possible_names,
    model='gpt-4'
)

# Resultado: ['João da Silva', 'Carlos Alberto']
```

### Reconhecimento de Datas

Pipeline customizado do Spacy para extração de datas:

```python
from date_spacy import find_dates

# Texto com datas
text = "Lei 12345 de 1º de dezembro de 2023"

# Extração de datas
nlp = spacy.blank("pt")
nlp.add_pipe('find_dates')
doc = nlp(text)

# Datas encontradas
dates = [ent._.date for ent in doc.ents]
```

### Processamento de Texto

```python
def sanitize_text(text: str) -> str:
    """Remove caracteres especiais e normaliza texto"""
    text = text.strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', ' ', text)
    return text
```

## 🔧 Configurações Avançadas

### Performance

#### Configuração de Workers
```python
# Em main.py
def parse_link_with_workers(self, data_rows: list, year: int, workers: int = 10):
    """Processa links em paralelo com múltiplos workers"""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for data_row in data_rows:
            future = executor.submit(self.parse_link, [data_row], None, year)
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
```

#### Configuração de Timeout
```python
# Timeout para requisições
TIMEOUT = 60  # segundos

# Delay entre requisições
DELAY_BETWEEN_REQUESTS = 1  # segundo

# Número de tentativas
RETRY_ATTEMPTS = 3
```

### Tratamento de Erros

#### Retry Automático
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry(self, url: str) -> Response:
    """Faz requisição com retry automático"""
    return self.session.get(url, timeout=TIMEOUT)
```

#### Logging Detalhado
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Playwright
```bash
# Reinstale o Playwright
playwright install --force

# Verifique se o Chromium está instalado
playwright install chromium
```

#### 2. Erro de Rate Limiting
```bash
# Aumente o delay entre requisições
export DELAY_BETWEEN_REQUESTS=5

# Reduza o número de workers
export WORKERS=5
```

#### 3. Erro de Memória
```bash
# Reduza o número de workers
export WORKERS=3

# Aumente a memória do Python
export PYTHONMALLOC=malloc
```

#### 4. Erro de Conexão
```bash
# Verifique a conectividade
curl -I https://www.planalto.gov.br

# Teste com proxy (se necessário)
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### Logs Úteis

#### Monitoramento de Progresso
```bash
# Logs em tempo real
tail -f crawler.log

# Estatísticas de progresso
grep "Processed" crawler.log | tail -10

# Erros encontrados
grep "ERROR" crawler.log
```

#### Verificação de Dados
```python
# Verifique os dados coletados
import pandas as pd

df = pd.read_csv('output/leis_ordinarias.csv')
print(f"Total de leis coletadas: {len(df)}")
print(f"Última atualização: {df['crawled_at'].max()}")
```

## 🚀 Deploy em Produção

### Docker Compose
```yaml
version: '3.8'

services:
  crawler-leis:
    build: ./leis-ordinarias
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - WORKERS=5
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  crawler-decretos:
    build: ./decretos-emendas
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - WORKERS=5
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  scheduler:
    image: mcuadros/ofelia:latest
    command: daemon --docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:rw
      - ./scheduler.ini:/etc/ofelia/config.ini
    restart: unless-stopped
```

### Agendamento com Cron
```bash
# Adicione ao crontab
0 2 * * * cd /path/to/legislatech-ai-crawlers/leis-ordinarias && python main.py
0 3 * * * cd /path/to/legislatech-ai-crawlers/decretos-emendas && python main.py
0 4 * * * cd /path/to/legislatech-ai-crawlers/medidas-provisorias && python main.py
```

### Monitoramento
```bash
# Script de monitoramento
#!/bin/bash
for crawler in leis-ordinarias decretos-emendas medidas-provisorias; do
    if [ ! -f "/tmp/${crawler}_last_run" ]; then
        echo "Crawler ${crawler} não executou hoje"
        # Enviar alerta
    fi
done
```

## 📈 Métricas e Performance

### Indicadores de Qualidade
- **Taxa de sucesso**: > 95% de páginas coletadas
- **Precisão de dados**: > 98% de campos corretos
- **Tempo de processamento**: < 2 horas para 1000 documentos
- **Uso de memória**: < 4GB por crawler

### Otimizações Implementadas
- **Processamento paralelo** com ThreadPoolExecutor
- **Cache de sessão** para evitar reautenticação
- **Retry inteligente** com backoff exponencial
- **Sanitização eficiente** de texto
- **Compressão de dados** para armazenamento

## 🤝 Contribuindo

### Adicionando um Novo Crawler

1. **Crie a estrutura**
   ```bash
   mkdir novo-crawler
   cd novo-crawler
   cp ../leis-ordinarias/* .
   ```

2. **Modifique main.py**
   ```python
   class Crawler:
       urls = {
           'main-page': 'https://site.oficial.gov.br',
       }
       
       def get_pages(self):
           # Implemente a lógica específica
           pass
   ```

3. **Teste o crawler**
   ```bash
   python main.py --test
   ```

4. **Adicione à documentação**
   - Atualize este README
   - Documente campos específicos
   - Adicione exemplos de uso

### Diretrizes de Desenvolvimento
- **Siga o padrão** dos crawlers existentes
- **Use type hints** em todas as funções
- **Adicione logs** detalhados
- **Implemente retry** para robustez
- **Teste com dados reais** antes do deploy

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 🆘 Suporte

### Canais de Ajuda
- **Documentação**: [docs.legisla.tech/crawlers](https://docs.legisla.tech/crawlers)
- **Email**: suporte@legisla.tech
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/legislatech-ai/issues)
- **Discord**: [Comunidade Legislatech](https://discord.gg/legislatech)

### FAQ

**Q: Como adicionar um novo tipo de legislação?**
A: Siga o template de leis-ordinarias e adapte para o novo tipo.

**Q: Como otimizar a performance?**
A: Ajuste o número de workers e delay entre requisições.

**Q: Como debugar problemas de scraping?**
A: Use logs detalhados e teste com `--debug` flag.

**Q: Como manter dados atualizados?**
A: Configure agendamento automático com cron ou Docker.

---

**Desenvolvido com ❤️ pela equipe Legislatech**

*Automatizando a coleta de legislação brasileira com inteligência artificial.*

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
