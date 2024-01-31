from kafka import KafkaConsumer
import json
import logging
import psycopg2
import datetime
import os
from config import IP_ADDRESS

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Retrieving environment variables
dbname = os.getenv('POSTGRES_DB')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('PORT')

logger.info('hahah', IP_ADDRESS)
# Kafka consumer connection
consumer = KafkaConsumer(
    'producer',
    bootstrap_servers=IP_ADDRESS+':9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    key_deserializer=lambda k: json.loads(k.decode('utf-8')),
)

# Loop for consuming messages
for message in consumer:
    try:

        # Connecting to PostgreSQL database
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        cursor = connection.cursor()
    
        # SQL query to insert coordinates into the database
        insert_query = '''
            INSERT INTO coordinates (ip, lat, lon, date) VALUES (%s, %s, %s, %s);
        '''
        
        # Getting current datetime in ISO format
        current_datetime = datetime.datetime.now().isoformat()

        # Executing the insert query with message data
        cursor.execute(insert_query, (message.key, message.value['lat'], message.value['lon'], current_datetime))

        # Committing the transaction
        connection.commit()
        
        # Logging successful insertion
        logger.info(f"Data inserted successfully! IP: {message.key}, Latitude: {message.value['lat']}, Longitude: {message.value['lon']}, Date: {current_datetime}")
    
        # Closing cursor and connection
        if connection:
            cursor.close()
            connection.close()   

    except Exception as e:
        # Logging error if insertion fails
        logger.info(f"Error: {e}")
        logger.info("Data not inserted due to errors")
