from cloudscraper import create_scraper
from requests.models import Response
from requests.cookies import RequestsCookieJar
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import threading
from sqlalchemy import create_engine
from agents import run_name_recognizer_agent
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import re
import spacy
import unicodedata
from date_spacy import find_dates #ignore
from dotenv import load_dotenv
import openai
import os
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
class Crawler:
    urls = {
        'law-page':'https://www4.planalto.gov.br/legislacao/portal-legis/legislacao-1/leis-delegadas-1',
    }

    openai_model = 'gpt-4.1-nano-2025-04-14'

    session: requests.Session
    def __init__(self):
        self._initialize_session_with_playwright()
        self.data = []
        self.date_nlp = self.setup_date_nlp()



    def setup_date_nlp(self):
        nlp = spacy.blank("pt")
        nlp.add_pipe('find_dates')
        return nlp



    @staticmethod
    def sanitize_text(text: str) -> str:
        text = text.strip()
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        text = re.sub(r'\s+', ' ', text)
        return text

    def _initialize_session_with_playwright(self):
        self.session = create_scraper()
        url_to_visit = self.urls['law-page']
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            try:
                page.goto(url_to_visit, timeout=60000)
                page.wait_for_selector('#portal-columns', timeout=30000)
                page.wait_for_load_state('networkidle', timeout=30000)
                playwright_cookies = context.cookies()
                if not self.session.cookies:
                    self.session.cookies = RequestsCookieJar()

                for cookie_dict in playwright_cookies:
                    self.session.cookies.set(
                        name=cookie_dict['name'],
                        value=cookie_dict['value'],
                        domain=cookie_dict['domain'],
                        path=cookie_dict['path'],
                        secure=cookie_dict['secure'],
                    )
            except Exception as e:
                print(f"Playwright: Erro durante a obtenção de cookies: {e}")
            finally:
                browser.close()

    def _do_get_page(self,url, args:dict=None)->Response:
        return self.session.get(url,params=args)

    def _do_post_page(self,url, data:dict=None)->Response:
        return self.session.post(url,data=data)


    def parse_link(self, data_rows:list, progress_bar)->None:
        for data_row in data_rows:
            tds = data_row.find_all('td')
            first_column = tds[0]
            second_column = tds[1]
            nome_lei = first_column.text
            link = first_column.find('a').get('href')
            ementa = second_column.text


            #a ordem dos fatores é sempre numero lei -> data publicacao -> (opcional) data publicacao dou
            parsed_string = ''
            parsed_words = []
            for word in nome_lei.split(" "):
                word = word.replace("P", " P")
                word = word.strip()
                if word == '':
                    continue
                elif not word.replace(".","").replace(",","").isdigit():
                    parsed_string += word + " "
                    continue

                word = self.sanitize_text(word)
                parsed_string += word + " "
                parsed_words.append(word.replace(",",""))
            if len(parsed_words) == 0:
                raise ValueError(f"Não foi possível encontrar o número da lei na string: {nome_lei}")
            num_lei = parsed_words[0]
            datas = self.date_nlp(parsed_string).ents

            try:data_lei = datas[0]._.date
            except:
                print(parsed_string)
                input('aperta aenter')
            if len(datas)> 1:
                data_dou = datas[1]._.date
            else:
                data_dou = None
            data_lei = data_lei.strftime("%Y-%m-%d")[2:]
            data_lei = '19'+data_lei
            _dict = {
                'num_lei': num_lei,
                'data_lei': data_lei,
                'data_dou': data_dou,
                'bleached_nome': parsed_string,
                'non_bleached_nome': nome_lei,
                'ementa': self.sanitize_text(ementa),
                'link': link,
            }

            lei_response = self.session.get(link)

            lei_response.raise_for_status()
            lei_text = lei_response.text
            lei_soup = BeautifulSoup(lei_text, 'html.parser')

            lei_string = ''
            non_parsed_lei_string = ''
            striked_string = ''
            non_parsed_striked_string = ''

            full_lei_string = ''
            non_parsed_full_lei_string = ''
            for paragraph_tag in lei_soup.find_all('p'):
                non_parsed_full_lei_string += paragraph_tag.text
                if paragraph_tag.find('strike'):
                    non_parsed_striked_string += paragraph_tag.text
                    text = self.sanitize_text(paragraph_tag.text)
                    if text == '':
                        continue
                    full_lei_string += text + "\n"
                    striked_string += text + "\n"
                    continue
                text = self.sanitize_text(paragraph_tag.text)
                if text == '':
                    continue
                lei_string += text + "\n"
                full_lei_string += text + "\n"
                non_parsed_lei_string += paragraph_tag.text + "\n"
            _dict['lei_text'] = lei_string
            _dict['non_parsed_lei_text'] = non_parsed_lei_string
            _dict['lei_text_striked'] = striked_string
            _dict['non_parsed_lei_text_striked'] = non_parsed_striked_string
            _dict['full_lei_text'] = full_lei_string
            _dict['non_parsed_full_lei_text'] = non_parsed_full_lei_string

            sanitized_sancionadores_tags = []

            for p_tag in lei_soup.find_all('p'):
                delimiter = '=_==*==_='

                for line_break in p_tag.find_all('br'):
                    line_break.replace_with(delimiter)
                text = p_tag.text.replace('\n', ' ').replace("\r", " ").replace("\t", " ").replace("   ", " ").replace("  ", " ").strip()
                text = unicodedata.normalize('NFKD',text).encode('ascii', 'ignore').decode('utf-8')
                if text:
                    texts = text.split(delimiter)

                    for text in texts:
                        pattern = 'senador|senadora|deputado|deputada'
                        ignore = re.compile(pattern, re.IGNORECASE)
                        text = ignore.sub('', text)
                        text = text.replace("*","")
                        text = text.strip()
                        if any(letter.isnumeric() for letter in text):
                            continue
                        elif text.strip() == '':
                            continue
                        elif '/' in text:
                            continue


                        sanitized_sancionadores_tags.append(text)

            possivel_other_sancionadores_nomes = []
            possivel_main_sancionadores = []

            #fazer assim pq as vezes tem 2 nomes iguais dai a key se repete
            names = {}
            for sancionador in sanitized_sancionadores_tags:
                key_name = sancionador.split(" ")[0].lower()
                if not names.get(key_name):
                    names[key_name] = sancionador.strip()
                else:
                    names[key_name] += "," + sancionador.strip()
            #names = {tag.split(" ")[0].lower():tag for tag in sanitized_sancionadores_tags}

            base_url = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/'
            full_url = f'{base_url}{"|".join(names.keys())}'
            request = self.session.get(full_url)
            try:name_data = request.json()
            except:
                print("Erro ao fazer a requisição para o IBGE")
                print(f"Link sancionadores: {link}")
                print(f"Nomes reconhecidos: {names}")
                print(f"Url nomes: {full_url}")
                input()
            for row in name_data:
                nome = row['nome']
                full_name = names.get(nome.lower())

                t_names = full_name.split(',')
                for full_name in t_names:
                    if full_name.isupper():
                        possivel_main_sancionadores.append(full_name)
                    else:
                        possivel_other_sancionadores_nomes.append(full_name)

            main_sancionador = "".join(run_name_recognizer_agent(possivel_main_sancionadores,self.openai_model))
            other_sancionadores = ",".join(run_name_recognizer_agent(possivel_other_sancionadores_nomes,self.openai_model))
            _dict['main_sancionador'] = main_sancionador
            _dict['other_sancionadores'] = other_sancionadores

            hard_coded_names = [
                'swenderberger',
                'macae',
                'onyx',
                'blairo',
                'cuido',
                'guido',
                'patrus',
                'humberto',
                'marlus',
                'martus',
                'ramez',
                'j.',
                'ibrahim',
                'delfim',
                'emane',
                'mailson',
                'armando',
            ]
            for name in hard_coded_names:
                if name in names:
                    _dict['other_sancionadores'] += "," + names[name]
            if len(_dict['other_sancionadores']) == 0:
                print('Sancionadores vazio: ', _dict['link'])
            self.data.append(_dict)
            progress_bar.update(1)

    def parse_link_with_workers(self, data_rows:list,  workers:int = 10):
        chunk_size = len(data_rows) // workers
        threads = []
        with tqdm(total=len(data_rows), desc="Parsing links") as progress_bar:
            for i in range(workers):
                start = i * chunk_size
                end = (i + 1) * chunk_size if i != workers - 1 else len(data_rows)
                thread = threading.Thread(target=self.parse_link, args=(data_rows[start:end], progress_bar))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        #debug sem thread
        # with tqdm(total=len(data_rows), desc="Parsing links") as progress_bar:
        #     self.parse_link(data_rows,progress_bar, year)

    def parse_year_pages(self, workers:int=10):
        self.data = []


        def run_parse_link(url, is_first_time:bool = True):
            html_response = self.session.get(url)
            html_response.raise_for_status()
            html = html_response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', {})
            if table:
                rows = table.find_all('tr', {})
                data_rows = rows[1:]
                self.parse_link_with_workers(data_rows, workers)


        run_parse_link(self.urls['law-page'])

        return self.data

if __name__ == "__main__":
    time_start = datetime.now()
    print(f"Time start: {time_start}")
    c = Crawler()
    workers = int(os.getenv('WORKERS', '1'))
    print("Obtendo páginas de anos...")
    print("Iniciando a raspagem das leis por ano...")
    laws = c.parse_year_pages(workers)
    df = pd.DataFrame(laws)
    df.to_csv('leis_delegadas.csv', sep=';')
    time_end = datetime.now()
    print(f"Time end: {time_end}")
    print(f"Time elapsed: {time_end - time_start}")



