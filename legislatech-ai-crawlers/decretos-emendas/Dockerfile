FROM python:3.12-slim

WORKDIR /app

COPY main.py /app/
COPY requirements.txt /app/
COPY date_spacy /app/date_spacy
COPY .env /app/

RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install

CMD ["python", "main.py"]