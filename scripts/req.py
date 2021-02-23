import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('../config/config.conf')

API_KEY = config['VARIABLES']['API_KEY']
# url = f'https://api.jcdecaux.com/vls/v3/contracts?apiKey={api_key}'


# result = json.loads(requests.get(url).text)

# print(type(result))
# for contract in result:
#     print(contract['name'])


URL = f'https://api.jcdecaux.com/vls/v3/stations?contract=toulouse&apiKey={API_KEY}'


result = json.loads(requests.get(URL).text)
compteur = 0
for station in result:
    print(station['contractName'])
    print(station['name'])
    print(station['totalStands']['availabilities']['bikes'])
    compteur += 1

print(compteur)