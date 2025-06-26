# routes/grafo.py
import time
import requests
import networkx as nx
from collections import deque
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import List
from fastapi import APIRouter, Query

router = APIRouter()

def criar_grafo_com_pagerank(urls_iniciais: List[str], profundidade_maxima: int = 1):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    G = nx.DiGraph()
    fila = deque([(url, 0) for url in urls_iniciais])
    visitados = set(urls_iniciais)

    while fila:
        source_url, profundidade_atual = fila.popleft()
        if profundidade_atual > profundidade_maxima:
            continue
        
        try:
            time.sleep(0.2) # Evita sobrecarregar o servidor
            response = requests.get(source_url, headers=headers, timeout=10)
            if response.status_code != 200: continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            G.add_node(source_url, profundidade=profundidade_atual)

            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                if not href or href.startswith(('#', 'javascript:')): continue
                
                absolute_url = urljoin(source_url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.netloc != urlparse(source_url).netloc: continue # Mantém no mesmo domínio
                
                clean_url = parsed_url._replace(query='', fragment='').geturl()
                if source_url != clean_url:
                    G.add_edge(source_url, clean_url)
                    if clean_url not in visitados:
                        visitados.add(clean_url)
                        fila.append((clean_url, profundidade_atual + 1))
        except requests.RequestException as e:
            print(f"Erro ao acessar {source_url}: {e}")
            continue

    if G.number_of_nodes() > 0:
        pagerank_scores = nx.pagerank(G, alpha=0.85)
        nx.set_node_attributes(G, pagerank_scores, 'pagerank')
    return G

@router.get("")
def gerar_grafo(
    urls: List[str] = Query(..., description="Lista de URLs iniciais para o crawling"),
    profundidade: int = Query(1, ge=0, le=2, description="Profundidade máxima do crawling"),
    top_n: int = Query(30, ge=10, le=100, description="Número de nós para retornar, ordenado por PageRank")
):
    grafo = criar_grafo_com_pagerank(urls, profundidade_maxima=profundidade)
    if grafo.number_of_nodes() == 0:
        return {"nodes": [], "links": []}

    pagerank = nx.get_node_attributes(grafo, "pagerank")
    ranking_ordenado = sorted(pagerank.items(), key=lambda item: item[1], reverse=True)
    
    top_nodes = {url for url, _ in ranking_ordenado[:top_n]}
    top_nodes.update(urls) # Garante que as URLs iniciais estejam no resultado
    
    subgrafo = grafo.subgraph(top_nodes)
    
    return {
        "nodes": [{"id": node, "pagerank": data.get("pagerank", 0), "group": 1 if node in urls else 2} for node, data in subgrafo.nodes(data=True)],
        "links": [{"source": src, "target": tgt} for src, tgt in subgrafo.edges()]
    }