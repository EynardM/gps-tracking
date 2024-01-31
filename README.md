# GPS Tracking with Apache Kafka, PostgreSQL, and React

Welcome to the GPS tracking project! This system utilizes Apache Kafka for communication between a producer and a consumer via a broker, a PostgreSQL database for storing data, a Python FastAPI for exposing this data, and a React frontend for displaying machine positions in real-time.

## Project Structure

1. **Kafka Broker (Kafka Server)**
   - Plays a central role in asynchronous communication between the producer and the consumer.

2. **Kafka Producer - Python Script**
   - Generates location data with machine IP addresses and sends it to the Kafka broker.

3. **Kafka Consumer - Python Script**
   - Receives data from the Kafka broker, stores it in a PostgreSQL database, and retrieves coordinates and IP addresses.

4. **PostgreSQL Database**
   - Stores coordinates and IP addresses of machines that have produced data in the Kafka broker.

5. **API (FastAPI)**
   - Retrieves data from the PostgreSQL database and exposes it via endpoints.

6. **WebSocket**
   - Facilitates bidirectional communication between the backend (API) and the frontend (React) to transmit data in real-time.

7. **React User Interface**
   - Connected to the WebSocket, it receives updated data from the server and displays it on a map.

## Configuration

- **Apache Kafka**
  - Configure the Kafka broker with appropriate topics.

- **PostgreSQL Database**
  - Ensure a PostgreSQL database is configured with necessary tables.

- **FastAPI API**
  - Configure the FastAPI API to connect to the database and expose necessary endpoints.

- **React User Interface**
  - Configure the React user interface to connect to the WebSocket.

## Running the Project

**The following commands should be executed in separate terminals. However, it is also possible to run all commands in the same terminal by adding the "-d" option. <br>Example for the first command: `docker compose -f broker-docker-compose.yml up --build -d`**

1. Start the Kafka broker: `docker compose -f broker-docker-compose.yml up --build` <br>
This will launch the Kafka broker that serves as a relay between the different producers.

2. Start the database: `docker compose -f psql-docker-compose.yml up --build` <br>
This Docker Compose will launch the database that serves as storage, in case the broker stops, and in our case, necessary for the API. Indeed, the database sends a notification to the API every time it receives a row.

3. Run the Kafka consumer: `docker compose -f consumer-docker-compose.yml up --build` <br>
The consumer will connect to the broker to retrieve data.

4. Run the Kafka producer: `docker compose -f producer-docker-compose.yml up --build` <br>
The producer will also connect to the broker to send data.

5. Start the FastAPI API: `docker compose -f api-docker-compose.yml up --build` <br>
The API will first create a WebSocket to the frontend. Then, every time it receives a notification from the database, it will send the received content over the WebSocket, which can then process the received data.

6. Start the React user interface that will connect to the WebSocket to display the data in real-time: `docker compose -f front-docker-compose.yml up --build` <br>
The user interface connects to the WebSocket to retrieve data. It then processes and displays the received information. (look at the video producer1-frontdocker-showingconsole.mp4)

## Stopping the Project

If you have executed all commands in separate terminals, you will need to do a "Ctrl + C" to stop the container. However, you will still need to stop your containers. <br>
Example for the stop command: `docker compose -f front-docker-compose.yml down`

## Access to the Database

It is possible to access the database via the following command: `psql -h localhost -p 5432 -U user -d amm_db`. Once connected to the database, several commands are available:
- Display the different tables present in the database: `\dt`
- Display the structure of the table: `\d coordinates`
- Display all data from the table: `SELECT * FROM coordinates;`


 ## Broker Configuration

### Local Deployment

If you intend to run the entire setup locally, follow these steps:

1. **Update IP Address:**
    - Open relevant files.
    - Change the IP address variable (in config.py and src/Components/Config.js and in the broker-docker-compose.yml).

### Networked Deployment

For separating the broker, consumer, and producers on the same network:

1. **Ensure Network Connectivity:**
    - All machines must be on the same network.

2. **Specify Broker's IP Address:**
    - Identify the machine running the broker.
    - Update the IP address variable in relevant files with the broker's machine IP (e.g., `172.17.10.1`).

### Files to Modify

1. **Python Files**
   - Configuration File: `config.py`
   - Update the IP address within this file.

2. **React Files**
   - Configuration File: `config.js`
   - Update the IP address within this file.

3. **Docker Compose**
   - Update the addresses in the environment section of the file `broker-docker-compose.yml`, in the following line `KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://172.17.10.1:9092,EXTERNAL://172.17.10.1:9093`. Change the 172.17.10.1 into the adress that you want.
   

## Little GIF to show a demo
   
![Gif that show the demo](KafkaProject.gif)

## Authors 

Florian Bergère </br>
Maxime Eynard </br>
Amaury Peterschmitt
