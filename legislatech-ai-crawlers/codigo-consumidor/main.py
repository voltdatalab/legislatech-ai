from pdfminer.high_level import extract_text
import os
import re
import pandas as pd
from sqlalchemy import create_engine
import requests
class Crawler:
    urls = {
        "pdf":"http://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/Anexos/cdc-portugues-2013.pdf"
    }

    def __init__(self):
        self.session  = requests.session()
        self.session.verify = False


    def get_pdf(self,file_name="temp.pdf"):
        with open(file_name, "wb") as f:
            response = self.session.get(self.urls["pdf"])
            if response.status_code == 200:
                f.write(response.content)
                print(f"PDF downloaded successfully as {file_name}")
            else:
                print(f"Failed to download PDF. Status code: {response.status_code}")

        text = extract_text(file_name)
        os.remove(file_name)
        return text

    def parse_pdf(self, text: str):
        #LEI Nº 8.078,
        #DE 11 DE SETEMBRO DE 1990

        pattern = r"((?: )\s*N[º°]\s*\d+(?:\.\d+)?(?:,\s*)?\s*DE\s*\d{1,2}\s+DE\s+[A-Za-zÀ-ÖØ-öø-ÿ]+\s+DE\s+\d{4})"

        parts = re.split(pattern, text)
        sections = []
        for i in range(1, len(parts), 2):
            section = parts[i] + parts[i + 1]
            if '..' not in section:
                sections.append(section)

        data = []
        for i, section in enumerate(sections):
            pattern = r"(?:LEI|DECRETO|PORTARIA|ANEXO)\s*N[º°]\s*(?P<number>\d+(?:\.\d+)?)(?:,\s*)?\s*DE\s*(?P<day>\d{1,2})\s+DE\s+(?P<month>[A-Za-zÀ-ÖØ-öø-ÿ]+)\s+DE\s+(?P<year>\d{4})"
            match = re.search(pattern, section, re.IGNORECASE)
            meses = {
                "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
                "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
                "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
            }
            if match:
                numero = match.group("number")
                dia = match.group("day")
                mes_texto = match.group("month").lower()
                ano = match.group("year")
                mes = meses.get(mes_texto, "00")
                _dict = {
                    "numero_lei":numero,
                    "data_lei": f"{dia}/{mes}/{ano}",
                    "texto":section,
                    "link":self.urls["pdf"]
                }
                data.append(_dict)
            else:
                raise Warning(f'Match not found for i={i}')
        return data


if __name__ == "__main__":
    #esse é desnecessáriop usar worker pela quantidade minima de dados
    crawler = Crawler()
    pdf_text = crawler.get_pdf()
    data = crawler.parse_pdf(pdf_text)
    df = pd.DataFrame(data)
    df.to_csv('codigo_consumidor.csv', index=False, encoding='utf-8')