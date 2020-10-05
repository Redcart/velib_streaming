import json
from kafka import KafkaConsumer
import psycopg2
import pandas as pd 
from connect_sql import config_sql

stations = {}
consumer = KafkaConsumer("velib-stations", bootstrap_servers='localhost:9092', group_id="velib-monitor-stations")
FEATURES = ["station_number", "station_adress", "contract", "available_bike_stands"]
df = pd.DataFrame(columns=FEATURES) 
parameters_sql = config_sql()
print(parameters_sql)
conn = psycopg2.connect(**parameters_sql)
print("SQL DataBase connection sucessful !")
cur = conn.cursor()

commands = [
"""
DROP TABLE IF EXISTS bikes_availabilty 
""",
"""
DROP TABLE IF EXISTS bikes_availabilty_temp 
""",
""" CREATE TABLE bikes_availabilty (
                station_number SERIAL PRIMARY KEY,
                station_adress VARCHAR(255) NOT NULL,
                contract VARCHAR(255) NOT NULL,
                available_bike_stands INT NOT NULL
                )
 """,
 """CREATE TABLE bikes_availabilty_temp (
                station_number SERIAL PRIMARY KEY,
                station_adress VARCHAR(255) NOT NULL,
                contract VARCHAR(255) NOT NULL,
                available_bike_stands INT NOT NULL
                )
"""
]
# create table one by one
for command in commands:
    cur.execute(command)
# close communication with the PostgreSQL database server
cur.close()
# commit the changes
conn.commit()
print('SQL tables created ! ')

for message in consumer:
    station_dico = dict()
    station_dico["station_number"] = list()
    station_dico["contract"] = list()
    station_dico["station_adress"] = list()
    station_dico["available_bike_stands"] = list()

    station = json.loads(message.value.decode())
    station_dico["station_number"].append(station["number"])
    station_dico["contract"].append(station["contractName"])
    station_dico["station_adress"].append(station["address"])
    station_dico["available_bike_stands"].append(station['totalStands']['availabilities']['bikes'])

    if station["contractName"] not in stations:
        stations[station["contractName"]] = {}
    city_stations = stations[station["contractName"]]
    if station["number"] not in city_stations:
        city_stations[station["number"]] = station['totalStands']['availabilities']['bikes']

    count_diff = station['totalStands']['availabilities']['bikes'] - city_stations[station["number"]]
    if count_diff != 0:
        city_stations[station["number"]] = station['totalStands']['availabilities']['bikes']
        print("{}{} {} ({})".format(
            "+" if count_diff > 0 else "",
            count_diff, station["address"], station["contractName"]
        ))
        
        df = df.append(pd.DataFrame.from_dict(station_dico))
        df.to_csv('stations_availabilities.csv', index=None)

        sql = """ INSERT INTO 
                  bikes_availabilty (station_adress, contract, available_bike_stands) 
                  VALUES(%s, %s, %s)
              """
        print((station["address"], station["contractName"], ))
        cur = conn.cursor()
        cur.execute(sql, (station["address"], station["contractName"], str(station['totalStands']['availabilities']['bikes'])))
        conn.commit()