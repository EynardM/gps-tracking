from fastapi import FastAPI, WebSocket
import psycopg2
import asyncio
import logging
import os

# Retrieving environment variables for PostgreSQL database connection
dbname = os.getenv('POSTGRES_DB')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('PORT')

# Initializing the FastAPI application
app = FastAPI()

# Configuring the logger
logger = logging.getLogger()

# Creating a lock for asynchronous operations on the WebSocket
websocket_lock = asyncio.Lock()

# WebSocket endpoint to listen for database notifications
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Connecting to the PostgreSQL database
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    logger.info('Connected to database')

    # Accepting the WebSocket connection
    await websocket.accept()

    while True:
        async with websocket_lock:
            with conn.cursor() as curs:
                # Listening for notifications on the 'coordinates_insert' channel
                curs.execute("LISTEN coordinates_insert;")
                conn.commit()

            # Checking for pending notifications
            if conn.notifies:
                notify = conn.notifies.pop(0)
                # Sending the notification payload to the WebSocket client
                await websocket.send_json(notify.payload)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "API is up and running"}
