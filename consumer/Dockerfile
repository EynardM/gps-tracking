FROM python:3.8

WORKDIR /app

COPY /consumer /app/consumer

COPY config.py /app/consumer/config.py

RUN pip install -r consumer/requirements.txt

CMD ["python", "consumer/consumer.py"]