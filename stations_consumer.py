import json
from kafka import KafkaConsumer
import psycopg2
from connect_sql import config_sql
from datetime import datetime

stations = {}
consumer = KafkaConsumer("velib-stations", bootstrap_servers='localhost:9092', group_id="velib-monitor-stations")
parameters_sql = config_sql()
conn = psycopg2.connect(**parameters_sql)
print("SQL DataBase connection sucessful !")
cur = conn.cursor()

commands = [
"""
DROP TABLE IF EXISTS bikes_availability 
""",
"""
DROP TABLE IF EXISTS bikes_availability_temp 
""",
""" CREATE TABLE bikes_availability (
                id SERIAL PRIMARY KEY,
                station_number INT,
                station_name VARCHAR(255) NOT NULL,
                station_adress VARCHAR(255) NOT NULL,
                contract VARCHAR(255) NOT NULL,
                capacity INT NOT NULL,
                nb_available_bikes INT NOT NULL,
                nb_available_bike_stands INT NOT NULL,
                time CHAR(19)
                )
 """,
 """CREATE TABLE bikes_availability_temp (
                id SERIAL PRIMARY KEY,
                station_number INT,
                station_name VARCHAR(255) NOT NULL,
                station_adress VARCHAR(255) NOT NULL,
                contract VARCHAR(255) NOT NULL,
                capacity INT NOT NULL,
                nb_available_bikes INT NOT NULL,
                nb_available_bike_stands INT NOT NULL,
                time CHAR(19)
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
        
        now = datetime.now()
        current_time = now.strftime("%Y/%d/%m %H:%M:%S")

        sql = """ INSERT INTO 
                  bikes_availability_temp (station_number, station_name, station_adress, contract, capacity, nb_available_bikes, nb_available_bike_stands, time) 
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
              """
        print((station["address"], station["contractName"], ))
        cur = conn.cursor()
        cur.execute(sql, (station["number"], station["name"], station["address"],  station["contractName"], str(station["totalStands"]["capacity"]), str(station["totalStands"]["availabilities"]["bikes"]), str(station["totalStands"]["availabilities"]["stands"]), current_time))
        conn.commit()