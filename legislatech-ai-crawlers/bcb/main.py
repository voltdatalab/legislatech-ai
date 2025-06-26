from cloudscraper import create_scraper
from bs4 import BeautifulSoup
import pandas as pd
import threading
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
class Crawler:
    tags = ['Todos', 'Ato de Diretor', 'Ato Normativo Conjunto', 'Ato do Presidente', 'Carta Circular', 'Circular',
            'Comunicado', 'Comunicado Conjunto', 'Decisão Conjunta', 'Instrução Normativa BCB',
            'Instrução Normativa Conjunta', 'Portaria Conjunta', 'Resolução BCB', 'Resolução CMN', 'Resolução Conjunta',
            'Resolução Coremec']
    api_endpoints = [
        'exibeoutrasnormas',
        'exibenormativo'
    ]
    urls = {
        'busca' : 'https://www.bcb.gov.br/api/search/app/normativos/buscanormativos',
        'api_text' : 'https://www.bcb.gov.br/api/conteudo/app/normativos/{endpoint}'
    }

    def __init__(self):
        self.session = create_scraper()

    def run_single_row(self, row, tag, worker_index):
        print(f"Worker: {worker_index}")
        params = {
            'p1': row['TipodoNormativoOWSCHCS'],
            'p2': row['NumeroOWSNMBR'].split(".")[0]
        }
        for endpoint in self.api_endpoints:
            link = self.urls['api_text'].format(endpoint=endpoint)
            info = self.session.get(link, params=params)
            data = info.json()
            conteudo = data.get('conteudo', [])
            if conteudo != []:
                for conteudo in conteudo:
                    try:
                        if conteudo['Assunto'] is not None:
                            conteudo['Assunto'] = BeautifulSoup(conteudo['Assunto'], 'html.parser').get_text().strip()
                        if conteudo['Texto'] is not None:
                            conteudo['Texto'] = BeautifulSoup(conteudo['Texto'], 'html.parser').get_text().strip()
                        conteudo['tag'] = tag
                        self.base_array.append(conteudo)
                        print(f"Processed content for tag '{tag}': {conteudo['Assunto']}")
                    except Exception as e:
                        print(f"Error processing content for tag '{tag}': {conteudo}, error: {e}                                                                    ")
                        continue

    def run(self, workers=5):
        self.base_array = []
        for tag in self.tags:
            start_row = 0
            while True:
                params = {
                    'querytext': f'ContentType:normativo AND contentSource:normativos AND TipodoNormativoOWSCHCS="{tag}"',
                    'rowlimit': 500,
                    'startrow': start_row,
                    'sortlist': 'Data1OWSDATE:descending',
                    'refinementfilters': 'Data:range(datetime(1980-06-15),datetime(2025-06-18T23:59:59))'
                }
                response = self.session.get(self.urls['busca'], params=params)
                response.raise_for_status()
                data = response.json()
                threads = []
                worker_index = 0
                for row in data['Rows']:
                    if worker_index >= workers:
                        for thread in threads:
                            thread.join()
                        threads = []
                        worker_index = 0
                    thread = threading.Thread(target=self.run_single_row, args=(row, tag, worker_index))
                    thread.start()
                    threads.append(thread)
                    worker_index += 1

                start_row += 500
                total_rows = data.get("TotalRows", 0)
                print(f"Fetched {len(self.base_array)} records for tag '{tag}' with total rows: {total_rows}")
                if total_rows < start_row + 500:
                    break
        df = pd.DataFrame(self.base_array)
        return df
if __name__ == '__main__':
    load_dotenv()
    crawler = Crawler()
    df = crawler.run(int(os.getenv('WORKERS', 5)))
