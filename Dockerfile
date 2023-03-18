FROM python:3.9.5-slim

WORKDIR /usr/local/pdf-creator

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY python python
COPY fonts fonts
COPY images images
COPY configs configs

COPY templates templates

COPY static static

EXPOSE 5050:5050

CMD python python/runner.py
