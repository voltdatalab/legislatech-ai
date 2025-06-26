from cloudscraper import create_scraper
from bs4 import BeautifulSoup
import re
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import threading
class crawler:
    urls = {
        "main":"https://anttlegis.antt.gov.br/action/ActionDatalegis.php"
    }

    def __init__(self):
        self.session = create_scraper()

    def do_couple_ementas(self, ementas):
        for ementa in ementas:
            data_tempo = None
            a_tag = ementa.find("a")
            endpoint = a_tag.get("href")

            link = f"{self.urls['main']}{endpoint}"

            response = self.session.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find("div", {"id": "conteudo"})
            ato = article.find("div", {"class": "ato"})

            ato_text = ato.get_text(strip=True)
            situacao = ementa.find("span", {"class": "ico-situacao"}).get_text(strip=True)
            titulo = a_tag.find("strong").get_text(strip=True)
            titulo = titulo.replace(situacao, "")

            data_pattern = r"(\d{1,2})\s+DE\s+([A-ZÇÃÕ]+)\s+DE\s+(\d{4})"
            match = re.search(data_pattern, titulo, re.IGNORECASE)
            if match:
                dia = match.group(1).zfill(2)
                mes_extenso = match.group(2).lower()
                ano = match.group(3)

                meses = {
                    "janeiro": "01",
                    "fevereiro": "02",
                    "março": "03",
                    "abril": "04",
                    "maio": "05",
                    "junho": "06",
                    "julho": "07",
                    "agosto": "08",
                    "setembro": "09",
                    "outubro": "10",
                    "novembro": "11",
                    "dezembro": "12"
                }
                mes = meses.get(mes_extenso, mes_extenso)
                data_tempo = f"{ano}-{mes}-{dia}"
            _dict = {
                "titulo": titulo.strip(),
                "data": data_tempo,
                "ato_texto": ato_text,
                "link": link
            }
            print(f"Processed record: {titulo.strip()} on {data_tempo}")
            print(f"Link: {link}")
            self.return_data.append(_dict)
        pass


    def run(self, workers=10):
        params = {
            "cod_modulo": "161",
            "cod_menu": "7804",
            "qtd_pagina":500,
        }
        self.return_data = []

        for year in range(2002, 2024):
            pagina = 1
            while True:
                print(f"Fetching data for year: {year}")
                start_paginas_acao = 'abrirResenhaAnoData'
                qtd_paginas_acao = 'informacaoRegistrosPaginaResenhaAno'
                informacao_paginas_acao = 'abrirPaginaResenhaAno'

                params['pagina'] = pagina
                params["ano"] = f"{year}"

                params['acao'] = start_paginas_acao
                response = self.session.get(self.urls["main"], params=params)
                response.raise_for_status()

                params['acao'] = qtd_paginas_acao
                response = self.session.get(self.urls["main"], params=params)
                response.raise_for_status()
                data = response.json()

                params['acao'] = informacao_paginas_acao
                response = self.session.get(self.urls["main"], params=params)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                ementas = soup.find_all("div", {'class':"ementa"})
                chunk_size = len(ementas) // workers
                threads = []
                for i in range(0, len(ementas), chunk_size):
                    ementas_chunk = ementas[i:i + chunk_size]
                    thread = threading.Thread(target=self.do_couple_ementas, args=(ementas_chunk,))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()


                if data['registroFinal'] >= data['totalRegistros']:
                    break
                pagina += 1
        return self.return_data

if __name__ == "__main__":
    load_dotenv()
    crawler = crawler()
    data = crawler.run(int(os.getenv('WORKERS', 5)))
    df = pd.DataFrame(data)