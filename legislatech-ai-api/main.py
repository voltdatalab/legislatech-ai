# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa os roteadores dos módulos de rotas
from routes import v1, v2, v3, grafo

app = FastAPI(
    title="RAG & Search API",
    description="API com endpoints para busca RAG, busca híbrida e crawling de grafos.",
    version="1.0.0"
)

# Adiciona o middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os roteadores na aplicação principal com seus respectivos prefixos
app.include_router(v1.router, prefix="/v1", tags=["V1 - Rerank Search"])
app.include_router(v2.router, prefix="/v2", tags=["V2 - Intent Router"])
app.include_router(v3.router, prefix="/v3", tags=["V3 - Generic Search"])
app.include_router(grafo.router, prefix="/grafo", tags=["Grafo Crawler"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bem-vindo à API de RAG Search + Completion"}