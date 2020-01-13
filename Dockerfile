FROM python:3.7.5-slim

WORKDIR /usr/local/pdf-creator

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py *.ttf *.svg *.txt ./

COPY templates templates

COPY static static

EXPOSE 5050:5050

CMD python runner.py
