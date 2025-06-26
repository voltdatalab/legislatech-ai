# routes/v1.py
import asyncio
import aiohttp
import json
import time
import uuid
from typing import AsyncGenerator
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from config import OPENAI_API_KEY, vector_store
from utils.auth import verify_basic_auth
from utils.sse import make_sse_event
from utils.prompt_helpers import _search_chunks, montar_contexto_com_documentos

router = APIRouter()

async def sse_simulate_response(query: str) -> AsyncGenerator[str, None]:
    """Lógica de streaming para a V1, com busca simples e geração de resposta."""
    sequence_number = -1
    def get_next_sequence_number():
        nonlocal sequence_number
        sequence_number += 1
        return sequence_number

    response_id = f"resp_{uuid.uuid4().hex}"
    message_item_id = f"msg_{uuid.uuid4().hex}"

    yield make_sse_event("response.created", {
        "type": "response.created", 
        "response": {"id": response_id, "status": "in_progress"}
    })
    await asyncio.sleep(0.05)
    
    # Usando o método assíncrono para buscar chunks
    search_chunks_result = await _search_chunks(query)
    annotations_list = []
    for i, link in enumerate(search_chunks_result.get("links", [])):
        annotation_payload = {"type": "url_citation", "title": search_chunks_result["titles"][i], "url": link}
        annotations_list.append(annotation_payload)
        yield make_sse_event("response.output_text.annotation.added", {
            "type": "response.output_text.annotation.added",
            "item_id": message_item_id, 
            "annotation": annotation_payload,
            "output_index": 1, 
            "content_index": 0,
            "annotation_index": i,
        })
        await asyncio.sleep(0.05)

    # Montagem do prompt e streaming da resposta do LLM
    prompt, erro = await montar_contexto_com_documentos(query, vector_store)
    if erro:
        yield make_sse_event("response.output_text.delta", {"delta": erro})
        return

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "stream": True, "temperature": 0, "messages": [{"role": "user", "content": prompt}]}
    
    full_text_content = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            async for line in resp.content:
                decoded = line.decode()
                if decoded.startswith("data: "):
                    json_data = decoded[len("data: "):].strip()
                    if json_data == "[DONE]": break
                    try:
                        j = json.loads(json_data)
                        content = j.get("choices", [{}])[0].get("delta", {}).get("content")
                        if content:
                            yield make_sse_event("response.output_text.delta", {
                                "type": "response.output_text.delta",
                                "item_id": message_item_id, 
                                "delta": content,
                                "output_index": 1,
                                "content_index": 0,
                            })
                            full_text_content += content
                            await asyncio.sleep(0.01)
                    except Exception:
                        continue
    
    yield make_sse_event("response.output_text.done", {
        "type": "response.output_text.done",
        "item_id": message_item_id, 
        "text": full_text_content
    })


@router.post("/responses", dependencies=[Depends(verify_basic_auth)])
async def simular_fluxo_response_generico(request: Request):
    body = await request.json()
    query = body.get("input", [{}])[-1].get("content", [{}])[0].get("text")
    if not query:
        raise HTTPException(status_code=400, detail="Query é obrigatória.")
    return StreamingResponse(sse_simulate_response(query), media_type="text/event-stream")