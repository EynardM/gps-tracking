FROM python:3.8

WORKDIR /app

COPY /producer /app/producer

COPY config.py /app/producer/config.py

RUN pip install -r producer/requirements.txt