from kafka import KafkaProducer
import requests  
import json
import time
import configparser

config = configparser.ConfigParser()
config.read('config.conf')

API_KEY = config['VARIABLES']['API_KEY']
URL = f'https://api.jcdecaux.com/vls/v3/stations?contract=toulouse&apiKey={API_KEY}'

producer = KafkaProducer(bootstrap_servers="localhost:9092")

while True:
    response = json.loads(requests.get(URL).text)
    for station in response:
        producer.send("velib-stations", json.dumps(station).encode())
    print("{} Produced {} station records".format(time.time(), len(response)))
    time.sleep(30)

# result = json.loads(requests.get(url).text.decode())
# compteur = 0
# for station in result:
#     producer.send("velib-stations", json.dumps(station).encode())
#     print(station['contractName'])
#     print(station['name'])
#     compteur += 1

# print(compteur)