# app/config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from tiktoken import get_encoding

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Chaves e Conexões ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

# --- Instâncias Globais ---

# Engine do SQLAlchemy com pool de conexões (síncrono)
engine = create_engine(
    CONNECTION_STRING,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Engine assíncrono do SQLAlchemy
async_engine = create_async_engine(
    CONNECTION_STRING.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Modelo de embeddings da OpenAI
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Vector Store (PGVector) como singleton assíncrono
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="michel_teste",
    connection=async_engine,
    use_jsonb=True
)

# Encoder para contagem de tokens
tiktoken_encoder = get_encoding("o200k_base")
