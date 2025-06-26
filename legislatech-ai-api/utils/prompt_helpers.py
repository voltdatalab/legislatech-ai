# utils/prompt_helpers.py
from config import tiktoken_encoder, vector_store, OPENAI_API_KEY
import aiohttp

def contar_tokens(texto: str) -> int:
    """Conta o número de tokens em um texto usando o encoder do tiktoken."""
    return len(tiktoken_encoder.encode(texto))

def adicionar_trechos(docs, limite_tokens):
    """
    Adiciona trechos de documentos a um contexto, respeitando um limite de tokens.
    """
    blocos, tokens = [], 0
    if not docs:
        return blocos, tokens
    
    for doc in docs:
        titulo = doc.metadata.get("titulo", "[Sem título]")
        doc_id = doc.metadata.get("id", "sem id")
        texto_limpo = doc.page_content.strip().replace("\n", " ")
        
        trecho_completo = f"- Título: {titulo} (ID: {doc_id})\nConteúdo: {texto_limpo}\n"
        trecho_tokens = contar_tokens(trecho_completo)

        if tokens + trecho_tokens > limite_tokens:
            texto_curto = texto_limpo[:int(len(texto_limpo)*0.5)] + "..."
            trecho_completo = f"- Título: {titulo} (ID: {doc_id})\nConteúdo: {texto_curto}\n"
            trecho_tokens = contar_tokens(trecho_completo)
            if tokens + trecho_tokens > limite_tokens:
                continue
        
        blocos.append(trecho_completo)
        tokens += trecho_tokens
    
    contexto_str = "\n".join(blocos)
    return contexto_str, tokens

async def buscar_contexto_enriquecido(docs_relevantes: list, vector_store) -> list:
    """
    Recebe uma lista de documentos relevantes e enriquece essa lista
    buscando o chunk inicial e os vizinhos de cada documento.
    """
    if not docs_relevantes:
        return []

    documentos_finais = {doc.metadata.get("id"): doc for doc in docs_relevantes}
    ids_adicionais_para_buscar = set()

    for doc in docs_relevantes:
        doc_id = doc.metadata.get("id")
        if not doc_id or "_" not in doc_id:
            continue

        try:
            prefixo, chunk_num_str = doc_id.rsplit("_", 1)
            chunk_num = int(chunk_num_str)
        except ValueError:
            continue

        if chunk_num > 0:
            id_chunk_zero = f"{prefixo}_0"
            if id_chunk_zero not in documentos_finais:
                ids_adicionais_para_buscar.add(id_chunk_zero)

        id_vizinho_1 = f"{prefixo}_{chunk_num + 1}"
        if id_vizinho_1 not in documentos_finais:
            ids_adicionais_para_buscar.add(id_vizinho_1)

        id_vizinho_2 = f"{prefixo}_{chunk_num + 2}"
        if id_vizinho_2 not in documentos_finais:
            ids_adicionais_para_buscar.add(id_vizinho_2)

    if ids_adicionais_para_buscar:
        try:
            # Usando o método assíncrono correto para buscar por IDs
            fetched_docs = await vector_store.aget_by_ids(list(ids_adicionais_para_buscar))

            for doc_adicional in fetched_docs:
                doc_id_adicional = doc_adicional.metadata.get("id")
                if doc_id_adicional not in documentos_finais:
                    documentos_finais[doc_id_adicional] = doc_adicional

        except Exception as e:
            print(f"⚠️ Erro ao buscar chunks adicionais: {e}")

    print(f"Total de documentos enriquecidos: {len(documentos_finais)}")

    return list(documentos_finais.values())

async def _search_chunks(query: str, k: int = 5) -> dict:
    """
    Busca chunks de documentos usando o retriever do vector_store.
    """
    print(f"Buscando chunks para a query: {query}")
    # Usando o método assíncrono correto para busca semântica
    docs = await vector_store.asimilarity_search(query, k=k)
    print(f"Encontrados {len(docs)} chunks para a query: {query}")
    
    return {
        "query": query,
        "chunk_ids": [doc.metadata.get("id") for doc in docs],
        "links": [doc.metadata.get("link") for doc in docs if doc.metadata.get("link")],
        "titles": [doc.metadata.get("titulo", "Sem título") for doc in docs],
        "documents": docs
    }

async def montar_contexto_com_documentos(query, vs, limite_contexto=4000, top_k=5):
    """
    Monta um contexto rico buscando documentos relacionados e formata o prompt.
    """
    # Usando o método assíncrono correto para busca semântica
    top_docs = await vs.asimilarity_search(query, k=top_k)
    
    contexto_str, _ = adicionar_trechos(top_docs, limite_contexto)
    
    prompt = f"""Se a pergunta do usuario for mais abrangente você deve responder de forma especifica, caso a pergunta do usuario seja muito especifica você pode responder com mais fluidez, seja acertivo mas sempre educado. Se a pergunta for em inglês responda em inglês. Use **apenas o contexto abaixo** para responder à pergunta.
Responda com uma lista de leis identificadas no contexto e faça uma **síntese breve de cada uma**.
Se a resposta não estiver claramente no contexto, diga: \"Não sei responder com base nos documentos fornecidos.\"
### Contexto:
{contexto_str}
### Pergunta:
{query}
### Resposta:"""
    return prompt, None

async def montar_contexto_e_gerar_resposta(query: str, docs_para_contexto: list, limite_contexto: int = 8000) -> str:
    """
    Pega uma lista de documentos, monta o contexto e cria o prompt final.
    """
    contexto_str, _ = adicionar_trechos(docs_para_contexto, limite_contexto)
    
    prompt = f"""Se a pergunta do usuario for mais abrangente você deve responder de forma especifica, caso a pergunta do usuario seja muito especifica você pode responder com mais fluidez, seja acertivo mas sempre educado. Se a pergunta for em inglês responda em inglês. Use **apenas o contexto abaixo** para responder à pergunta.
Responda com uma lista de leis identificadas nos documentos abaixo e faça uma **síntese breve de cada uma**.
### Documentos:
{contexto_str}
### Pergunta:
{query}
### Resposta:"""
    print(f"Prompt gerado com {contar_tokens(prompt)} tokens.")
    if contar_tokens(prompt) > limite_contexto:
        print("⚠️ O prompt gerado excede o limite de tokens permitido.")

    return prompt

async def expandir_query(query: str) -> list:
    """
    Expande uma query gerando variações e termos relacionados usando GPT-4.
    """
    prompt = f"""Gere 3 variações da seguinte pergunta, mantendo o significado principal mas usando diferentes palavras e estruturas:
    Pergunta original: {query}
    
    Retorne apenas as variações, uma por linha, sem numeração ou marcadores."""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150
            }
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as resp:
                resp.raise_for_status()
                variations = (await resp.json())["choices"][0]["message"]["content"].strip().split("\n")
                return [query] + [v.strip() for v in variations if v.strip()]
    except Exception as e:
        print(f"Erro ao expandir query: {e}")
        return [query]

async def recursive_retrieval(query: str, vector_store, max_depth: int = 2) -> list:
    """
    Implementa busca recursiva, gerando sub-queries baseadas nos resultados iniciais.
    """
    all_docs = []
    current_docs = await vector_store.asimilarity_search(query, k=5)
    all_docs.extend(current_docs)
    
    if not current_docs or max_depth <= 0:
        return all_docs
    
    # Gerar sub-queries baseadas nos resultados
    context = "\n".join([doc.page_content for doc in current_docs[:3]])
    sub_query_prompt = f"""Com base no seguinte contexto, gere 2 perguntas específicas que ajudariam a encontrar mais informações relevantes:
    
    Contexto:
    {context}
    
    Pergunta original: {query}
    
    Retorne apenas as perguntas, uma por linha, sem numeração."""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": sub_query_prompt}],
                "max_tokens": 150
            }
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as resp:
                resp.raise_for_status()
                sub_queries = (await resp.json())["choices"][0]["message"]["content"].strip().split("\n")
                
                # Buscar documentos para cada sub-query
                for sub_query in sub_queries:
                    sub_query = sub_query.strip()
                    if sub_query:
                        sub_docs = await recursive_retrieval(sub_query, vector_store, max_depth - 1)
                        all_docs.extend(sub_docs)
    except Exception as e:
        print(f"Erro na busca recursiva: {e}")
    
    return all_docs