FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 15010

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "15010"]