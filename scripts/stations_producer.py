import json
import time
import configparser
from kafka import KafkaProducer
import requests  

config = configparser.ConfigParser()
config.read('../config/config.conf')

API_KEY = config['VARIABLES']['API_KEY']
CONTRACT_NAME = config['VARIABLES']['CONTRACT_NAME']
URL = f"https://api.jcdecaux.com/vls/v3/stations?contract={CONTRACT_NAME}&apiKey={API_KEY}"

producer = KafkaProducer(bootstrap_servers="localhost:9092")

while True:
    response = json.loads(requests.get(URL).text)
    for station in response:
        producer.send("velib-stations", json.dumps(station).encode('utf-8'), key=str(station["number"]).encode('utf-8'))

    time.sleep(1)
