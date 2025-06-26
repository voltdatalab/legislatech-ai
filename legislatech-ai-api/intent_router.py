import aiohttp
import json
from sqlalchemy import text

class IntentRouter:
    # A função __init__ e decide_intent continuam as mesmas.
    def __init__(self, openai_api_key, engine):
        self.api_key = openai_api_key
        self.engine = engine

    async def decide_intent(self, user_query: str) -> dict:
        # (Nenhuma alteração aqui, o código continua o mesmo da versão anterior)
        meta_prompt = f"""
Você é um assistente especialista em traduzir perguntas em linguagem natural para um JSON estruturado que será usado para consultar um banco de dados de leis.

A tabela 'langchain_pg_embedding' tem duas colunas importantes para a busca:
1. `document` (TEXT): O conteúdo completo do chunk da lei.
2. `cmetadata` (JSONB): Metadados com os seguintes campos:
    - `titulo` (text): O título completo da lei.
    - `ano` (integer): Ano de publicação.
    - `num_lei` (float): O número da lei.
    - `data_lei` (text, formato 'YYYY-MM-DD').
    - `main_sancionador` (text): Nome de quem sancionou.
    - `tipo` (text): Ex: 'mpv', 'lei ordinaria'.

**Regra de Decisão Principal:**
- Use `"use_sql": true` para perguntas que pedem para **listar, contar, encontrar, ou filtrar** documentos com base em seus metadados (ex: "quais leis", "quantas leis", "encontre a lei X").
- Use `"use_sql": false` para perguntas que pedem para **explicar, resumir, ou dizer do que trata** uma lei. Essas perguntas exigem a leitura do conteúdo e devem ser respondidas via busca semântica (RAG).

Seu formato de resposta DEVE ser apenas um JSON válido.

Exemplo 1: "quais leis o geraldo alckmin sancionou em 2024 sobre agrotóxicos?"
JSON esperado:
{{
  "use_sql": true,
  "filters": {{"ano": 2024, "main_sancionador": "GERALDO JOSE RODRIGUES ALCKMIN FILHO"}},
  "text_search_terms": ["agrotóxicos"],
  "select_fields": ["titulo", "link"],
  "aggregation": "list"
}}

Exemplo 2: "conte todas as MPs de 2023 sobre o setor elétrico"
JSON esperado:
{{
  "use_sql": true,
  "filters": {{"ano": 2023, "tipo": "mpv"}},
  "text_search_terms": ["setor elétrico"],
  "select_fields": ["titulo"],
  "aggregation": "count"
}}

Exemplo 3: "Do que trata a lei nº 14.129?"
JSON esperado:
{{ "use_sql": false }}

Exemplo 4: "qual a importância do código civil?"
JSON esperado:
{{ "use_sql": false }}

Agora, analise a pergunta do usuário e retorne APENAS o JSON correspondente.

Pergunta do usuário:
\"\"\"{user_query}\"\"\"
"""
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": meta_prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload
            ) as resp:
                resp.raise_for_status()
                resp_json = await resp.json()
                content = resp_json["choices"][0]["message"]["content"]
                return json.loads(content)


    # ATUALIZAÇÃO PRINCIPAL AQUI
    def run_sql(self, sql_decision: dict) -> dict:
        """
        Executa a query SQL e formata o resultado como um texto amigável.
        """
        filters = sql_decision.get("filters", {})
        text_terms = sql_decision.get("text_search_terms", [])
        select_fields = sql_decision.get("select_fields", ["titulo", "link"])
        aggregation = sql_decision.get("aggregation", "list")

        where_clauses = []
        params = {}
        
        for k, v in filters.items():
            param_key = f"filter_{k}"
            where_clauses.append(f"cmetadata->>'{k}' = :{param_key}")
            params[param_key] = str(v)

        for i, term in enumerate(text_terms):
            param_key = f"term_{i}"
            where_clauses.append(f"(cmetadata->>'titulo' ILIKE :{param_key} OR document ILIKE :{param_key})")
            params[param_key] = f"%{term}%"

        where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"

        if aggregation == "count":
            sql = f"SELECT COUNT(DISTINCT SPLIT_PART(cmetadata->>'id', '_', 1)) AS total FROM langchain_pg_embedding WHERE {where_sql};"
        else:
            # Garante que 'titulo' e 'link' estejam sempre presentes para a formatação
            if 'titulo' not in select_fields: select_fields.append('titulo')
            if 'link' not in select_fields: select_fields.append('link')
            
            select_expr = ", ".join([f"cmetadata->>'{f}' AS {f}" for f in select_fields])
            sql = f"SELECT DISTINCT {select_expr} FROM langchain_pg_embedding WHERE {where_sql} LIMIT 20;"

        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params).fetchall()
            
            # Formatação da saída para texto
            if aggregation == "count":
                count = result[0][0]
                return {"resultado": f"Encontrei **{count}** documentos que correspondem aos seus critérios de busca."}
            else:
                rows = [dict(row._mapping) for row in result]
                if not rows:
                    return {"resultado": "Não encontrei nenhum documento que corresponda à sua pesquisa."}
                
                # Constrói a resposta em Markdown
                resposta_formatada = "Encontrei os seguintes documentos para você:\n\n"
                for row in rows:
                    titulo = row.get('titulo', 'Título não disponível')
                    link = row.get('link', '#')
                    resposta_formatada += f"- **{titulo.strip()}**\n  - [Acessar texto completo]({link})\n"
                
                return {"resultado": resposta_formatada}