from requests import session
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import re
import os
import pandas as pd
from uuid import uuid4
from sqlalchemy import create_engine
import subprocess
import threading
from dotenv import load_dotenv
import os
class Crawler:
    urls = {
        'main':'https://www.ana.gov.br/www2/resolucoes/'
    }

    def __init__(self):
        self.session = session()
        self.session.verify = False

    def process_chunk(self, resolucoes, year:int):
        for resolucao in resolucoes:
            file_name = uuid4().hex
            titulo_resolucao = resolucao.find("div",{"class":"titulo_resolucao"}).find('a',{"class":"lnk_resolucao"}).find("b").get_text(strip=True)

            pdf = resolucao.find('a', {'class':"ico_pdf"})
            if not pdf:
                print(f"No PDF link found for resolution: {titulo_resolucao} no ano {year}")
                continue
            pdf = pdf['onclick']
            pattern = r"abreArquivo\('([^']+)'\)"
            match = re.search(pattern, pdf)
            assert match, "Failed to find PDF link in the resolution"
            viewer_pdf_link = match.group(1)
            pdf_link:str = viewer_pdf_link.split('?file=', 1)[-1]
            if not pdf_link.startswith('http'):
                base_url = 'https://arquivos.ana.gov.br'
                pdf_link = base_url + pdf_link
            print(f"Found PDF link: {pdf_link}")
            with open(f'{file_name}.pdf', 'wb') as f:
                pdf_response = self.session.get(pdf_link)
                if pdf_response.status_code != 200:
                    print("Failed to download PDF")
                    continue
                #assert pdf_response.status_code == 200, "Failed to download PDF"
                f.write(pdf_response.content)
            command = [
                "gswin32c.exe",
                "-o", f"{file_name}.pdf",
                "-sDEVICE=pdfwrite",
                f"{file_name}.pdf"
            ]
            subprocess.run(command)

            print(f"Downloaded PDF for {titulo_resolucao}")
            full_text = extract_text(f"{file_name}.pdf")
            print(f"Extracted text from PDF for {titulo_resolucao}")
            _dict = {
                'titulo_resolucao': titulo_resolucao,
                'pdf_link': pdf_link,
                'full_text': full_text
            }
            self.data.append(_dict)
            os.remove(f'{file_name}.pdf')

    def run(self, year:int, workers=5):
        print("Fetching main page...")
        payload = {
            'cmbAno':f"{year}",
            'rdVisualizacao':'sequencial',
            'txt_busca':''
        }
        print(f"fetching year {year}")
        self.data = []

        for n in range(10):
            response = self.session.post(self.urls['main'], data=payload)
            if response.status_code == 200:
                break

            if n == 9:
                #raise Exception(f"Failed to fetch data for year {year} after multiple attempts")
                #2014 ta com erro no backend deles
                return self.data
        soup = BeautifulSoup(response.text, 'html.parser')
        resolucoes = soup.find_all('div',{"class":"resolucao"})
        chunk_size = len(resolucoes) // workers + 1
        print(f"Found {len(resolucoes)} resolutions for year {year}, processing in chunks of {chunk_size}...")
        threads = []
        for i in range(0, len(resolucoes), chunk_size):
            chunk = resolucoes[i:i + chunk_size]
            thread = threading.Thread(target=self.process_chunk, args=(chunk, year))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()


        print(f"Total resolutions found for year {year}: {len(data)}")
        return self.data


if __name__ == '__main__':
    load_dotenv()
    crawler = Crawler()
    years = range(2002, 2025)
    data = []
    for year in years:
        _data = crawler.run(year, int(os.getenv('WORKERS', 5)))
        data.extend(_data)
    df = pd.DataFrame(data)
    df.to_csv('resolucoes_ana.csv', index=False, encoding='utf-8')
