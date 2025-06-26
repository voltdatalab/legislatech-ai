from cloudscraper import create_scraper
from bs4 import BeautifulSoup, element
from pdfminer.high_level import extract_text
import pandas as pd
from sqlalchemy import create_engine
import os
class Crawler:

    urls = {
        'start':'https://www.congressonacional.leg.br/legislacao-e-publicacoes/regimento-do-congresso-nacional'
    }

    def __init__(self):
        self.session = create_scraper()

    @staticmethod
    def parse_paragraphs(paragraphs:list[str], link:str, name:str)->list[str]:
        artigos = []
        current_str = ''

        for p_text in paragraphs:
            if 'art. ' in p_text.lower():
                _dict = {
                    'link': link,
                    'name': name,
                    'artigo': current_str
                }
                artigos.append(_dict)
                current_str = p_text
            else:
                current_str += ' ' + p_text
        # fazer o insert final pra pegar a ultima current_str
        _dict = {
            'link': link,
            'name': name,
            'artigo': current_str
        }
        artigos.append(_dict)
        return artigos



    def run(self)-> pd.DataFrame:
        sopa = BeautifulSoup(self.session.get(self.urls['start']).text, 'html.parser')
        conteudos = sopa.find_all('div',{'class':"tabelaBotaoconteudo"})
        file_links = []
        html_links = []
        file_extensions = ['pdf', 'epub', 'doc', 'rtf']
        for conteudo in conteudos:
            links = conteudo.find_all('a')
            for link in links:
                if not link['href'].startswith('http'):
                    continue

                if any(file_ext in link['href'] for file_ext in file_extensions):
                    file_links.append((link['href'], link.get_text()))
                    print(link['href'])
                    print("File link found:", link.get_text())
                elif 'camara.leg.br' in link['href']:
                    #aqui ta fazendo isso pq o camara.leg só vai ter arquivo, n tem paginas
                    continue
                else:
                    html_links.append((link['href'], link.get_text()))
        artigos = []
        for link, name in html_links:
            text = self.session.get(link).text
            soup = BeautifulSoup(text, 'html.parser')
            conteudo = soup.find('div',{"id":"conteudoPrincipal"})
            if not conteudo:
                input(link)
                continue
            paragraphs = conteudo.find_all('p')
            t_artigos = self.parse_paragraphs([p.get_text() for p in paragraphs], link, name)
            artigos.extend(t_artigos)

        #parte dos files
        for file_extension in file_extensions:
            links = [
                l for l in file_links if file_extension in l[0].lower()
            ]
            for link, name in links:
                file_name = f"temp.{file_extension}"



                if file_extension == 'pdf':
                    with open(file_name, 'wb') as f:
                        f.write(self.session.get(link).content)
                    text = extract_text(file_name)
                    t_artigos = self.parse_paragraphs(
                        text.split('\n'),
                        link,
                        name
                    )
                    artigos.extend(t_artigos)
                    os.remove(file_name)
        df = pd.DataFrame(artigos)
        return df
if __name__ == "__main__":
    #aqui não tem workers pela quantidade de arquivos minimos
    crawler = Crawler()
    df = crawler.run()
    df.to_csv('regimento_congresso.csv', index=False, encoding='utf-8')
