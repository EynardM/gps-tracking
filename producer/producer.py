import argparse
import logging
import time
import random
import socket
from kafka import KafkaProducer
import json 
import math 
from config import IP_ADDRESS

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Function that will update coordinates 
def near_coordinate_generation(coordinates, radius, bearing):
    latitude, longitude = coordinates
    
    # Convert angle to radians
    bearing = math.radians(bearing)
    
    # Add random angle for variability in direction
    random_angle = random.uniform(0, math.pi * 2)  # Random angle between 0 and 2*pi radians
    bearing += random_angle
    
    # Convert distance to degrees of latitude and longitude
    delta_lat = radius / 111.32  # 1 degree of latitude ≈ 111.32 km
    delta_lon = radius / (111.32 * math.cos(math.radians(latitude)))  # 1 degree of longitude ≈ 111.32 km * cos(latitude)
    
    # Calculate adjustment factor for random movements based on angle
    lat_factor = math.cos(bearing)
    lon_factor = math.sin(bearing)
    
    # Calculate random movements in each direction
    random_lat = random.uniform(0, delta_lat) * lat_factor
    random_lon = random.uniform(0, delta_lon) * lon_factor
    
    # Calculate new coordinates
    new_latitude = latitude + random_lat
    new_longitude = longitude + random_lon
    
    # Round coordinates
    new_latitude = round(new_latitude, 6)
    new_longitude = round(new_longitude, 6)
    
    return new_latitude, new_longitude

# Modify ip to identify each producer
def modify_ip(broker_key):
    ip_parts = IP_ADDRESS.split('.')
    ip_parts[-1] = str(broker_key)
    new_ip = '.'.join(ip_parts)
    return new_ip

# Parse command line arguments
parser = argparse.ArgumentParser(description='Kafka Producer')
parser.add_argument('--service-name', type=str, required=True, help='Service name')
args = parser.parse_args()

# Get the producer 
service_name = args.service_name
broker_key = int(service_name[-1])
local_ip_address = modify_ip(broker_key)+':9092'

coordinates = [-73.49491815199443, 169.6962659072567]
bearings = [0, 90, 180, 270]

# Kafka Producer configuration
producer = KafkaProducer(
    bootstrap_servers=IP_ADDRESS+':9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: json.dumps(k).encode('utf-8'),
)

try:
    while True:
        # Generate new coordinates near the original coordinates
        new_coordinates = near_coordinate_generation(coordinates, radius=1.5, bearing=bearings[broker_key - 1])
        logger.info(f"Coordinates: {new_coordinates}")
        
        # Set partition key as local IP address
        partition_key = local_ip_address
        logger.info(local_ip_address)

        # Create dictionary of coordinates
        coordinates_dict = {'lat': new_coordinates[0], 'lon': new_coordinates[1]}
        logger.info(f"Service: {service_name}, Key: {partition_key}, Value: {coordinates_dict}")
        
        # Send message to Kafka topic
        producer.send('producer', key=partition_key, value=coordinates_dict)
        
        # Wait for 2 seconds before sending the next message
        time.sleep(2)

except KeyboardInterrupt:
    logger.info("Producer stopped by user.")

finally:
    producer.close()
