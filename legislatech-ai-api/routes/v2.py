# routes/v2.py
import asyncio
import aiohttp
import json
import uuid
import itertools
from typing import AsyncGenerator
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from langchain.retrievers import BM25Retriever
from config import OPENAI_API_KEY, vector_store
from utils.auth import verify_basic_auth
from utils.sse import make_sse_event
from utils.prompt_helpers import (
    montar_contexto_e_gerar_resposta, 
    buscar_contexto_enriquecido, 
    expandir_query,
    recursive_retrieval
)
import hashlib
from functools import lru_cache


router = APIRouter()

# Cache simples para resultados
@lru_cache(maxsize=100)
def get_cache_key(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()

async def rerank_search_sse(query: str, original_query: str) -> AsyncGenerator[str, None]:
    """Lógica de streaming para V2 e V3, com busca híbrida, rerank e geração."""
    response_id = f"resp_{uuid.uuid4().hex}"
    message_item_id = f"msg_{uuid.uuid4().hex}"
    
    yield make_sse_event("response.created", {"type": "response.created", "response": {"id": response_id, "status": "in_progress"}})
    
    # Expandir a query
    expanded_queries = await expandir_query(query)
    print(f"Queries expandidas: {expanded_queries}")
    
    # --- FASE 1: BUSCA HÍBRIDA COM QUERIES EXPANDIDAS E RECURSIVA ---
    all_semantic_docs = []
    for q in expanded_queries:
        # Busca semântica normal
        docs = await vector_store.asimilarity_search(q, k=30)
        all_semantic_docs.extend(docs)
        
        # Busca recursiva
        recursive_docs = await recursive_retrieval(q, vector_store)
        all_semantic_docs.extend(recursive_docs)
    
    if not all_semantic_docs:
        yield make_sse_event("response.output_text.delta", {"delta": "Nenhum documento relevante foi encontrado."})
        return
        
    # Remover duplicatas mantendo a ordem
    seen_ids = set()
    unique_docs = []
    for doc in all_semantic_docs:
        doc_id = doc.metadata.get("id")
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            unique_docs.append(doc)
    
    bm25_retriever = BM25Retriever.from_documents(unique_docs)
    keyword_docs = bm25_retriever.invoke(query)
    final_candidates = list({doc.page_content: doc for doc in itertools.chain(keyword_docs, unique_docs)}.values())
    docs_for_llm_rerank = final_candidates[:20]

    # --- FASE 2: RERANK COM LLM ---
    formatted_chunks = [f"[{i+1}] {doc.page_content[:300]}..." for i, doc in enumerate(docs_for_llm_rerank)]
    rerank_instruction = f"Analise os trechos a seguir e escolha os 5-10 mais relevantes para a pergunta: '{query}'. Retorne apenas os números dos trechos, separados por vírgula.\n\n" + "\n".join(formatted_chunks)
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    rerank_payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": rerank_instruction}], "max_tokens": 50}
    
    selected_chunks = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=rerank_payload) as resp:
                resp_json = await resp.json()
                selected_indexes = [int(x.strip()) - 1 for x in resp_json["choices"][0]["message"]["content"].split(',') if x.strip().isdigit()]
                selected_chunks = [docs_for_llm_rerank[i] for i in selected_indexes if i < len(docs_for_llm_rerank)]
    except Exception as e:
        print(f"Erro no rerank, usando fallback. Erro: {e}")
        selected_chunks = docs_for_llm_rerank[:5]


    docs_enriquecidos = await buscar_contexto_enriquecido(selected_chunks, vector_store)
    
    # --- FASE 3: GERAÇÃO DA RESPOSTA ---
    annotations_list = []
    for i, doc in enumerate(docs_enriquecidos):
        annotation_payload = {"type": "url_citation", "title": doc.metadata.get("titulo", "[Sem título]"), "text": f"Fonte {i+1}", "url": doc.metadata.get("link", "-")}
        annotations_list.append(annotation_payload)
        yield make_sse_event("response.output_text.annotation.added", {
            "type": "response.output_text.annotation.added",
            "item_id": message_item_id,
            "output_index": 1,
            "content_index": 0,
            "annotation_index": i,
            "annotation": annotation_payload
        })
        await asyncio.sleep(0.05)

    final_prompt = await montar_contexto_e_gerar_resposta(original_query, docs_enriquecidos)
    generation_payload = {"model": "gpt-4o-mini", "stream": True, "temperature": 0, "messages": [{"role": "user", "content": final_prompt}]}

    full_text_content = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=generation_payload) as resp:
            async for line in resp.content:
                if line.strip().endswith(b"[DONE]"): break
                if line.startswith(b"data: "):
                    try:
                        content = json.loads(line[6:])["choices"][0]["delta"].get("content")
                        if content:
                            yield make_sse_event("response.output_text.delta", {
                                "type": "response.output_text.delta",
                                "item_id": message_item_id,
                                "output_index": 1,
                                "content_index": 0,
                                "delta": content
                            })
                            full_text_content += content
                            await asyncio.sleep(0.01)
                    except (json.JSONDecodeError, IndexError, KeyError):
                        continue

    yield make_sse_event("response.output_text.done", {
        "type": "response.output_text.done",
        "item_id": message_item_id, 
        "text": full_text_content
    })

@router.post("/responses", dependencies=[Depends(verify_basic_auth)])
async def rerank_search_endpoint(request: Request):
    body = await request.json()
    user_query = body.get("input", [{}])[-1].get("content", [{}])[0].get("text")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query é obrigatória.")
    
    # Refinar a query antes da busca
    refined_query = user_query # Fallback
    refine_prompt = f"Reescreva a seguinte pergunta para otimizar a busca em um sistema de rag sobre as leis do brasil: {user_query}"
    print(f"Refinando query: {refine_prompt}")
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": refine_prompt}], "max_tokens": 128}
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as resp:
                resp.raise_for_status()
                refined_query = (await resp.json())["choices"][0]["message"]["content"].strip()
        print(f"Query refinada: {refined_query}")
    except Exception as e:
        print(f"Erro ao refinar query: {e}")

    return StreamingResponse(rerank_search_sse(query=refined_query, original_query=user_query), media_type="text/event-stream")
    
    