#!/home/redcart/Data_Science/velib_streaming/streaming/bin/python

import json
from datetime import datetime
import configparser
import argparse
import requests  
import psycopg2
from kafka import KafkaProducer

from connect_sql import config_sql

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', dest='mode', type=str, default='overwrite',
                        help='output mode (overwrite or append). Set to overwrite by default.')


    args = parser.parse_args()
    MODE = args.mode

    API_KEY = config['VARIABLES']['API_KEY']
    CONTRACT_NAME = config['VARIABLES']['CONTRACT_NAME']
    URL = f"https://api.jcdecaux.com/vls/v3/stations?contract={CONTRACT_NAME}&apiKey={API_KEY}"

    parameters_sql = config_sql()
    conn = psycopg2.connect(**parameters_sql)
    print("SQL DataBase connection sucessful !")

    if MODE == 'overwrite':

        cur = conn.cursor()

        commands = [
        """
        DROP TABLE IF EXISTS stations_info
        """,
        """
        DROP TABLE IF EXISTS stations_info_temp 
        """,
        """ CREATE TABLE stations_info (
                        id SERIAL PRIMARY KEY,
                        station_number INT,
                        station_name VARCHAR(255) NOT NULL,
                        station_adress VARCHAR(255) NOT NULL,
                        contract VARCHAR(255) NOT NULL,
                        latitude DOUBLE PRECISION NOT NULL,
                        longitude DOUBLE PRECISION NOT NULL,
                        banking BOOLEAN NOT NULL, 
                        status VARCHAR(6) NOT NULL, 
                        connected BOOLEAN NOT NULL,
                        time CHAR(19)
                        )
        """,
        """ CREATE TABLE stations_info_temp (
                        id SERIAL PRIMARY KEY,
                        station_number INT,
                        station_name VARCHAR(255) NOT NULL,
                        station_adress VARCHAR(255) NOT NULL,
                        contract VARCHAR(255) NOT NULL,
                        latitude DOUBLE PRECISION NOT NULL,
                        longitude DOUBLE PRECISION NOT NULL,
                        banking BOOLEAN NOT NULL, 
                        status VARCHAR(6) NOT NULL, 
                        connected BOOLEAN NOT NULL,
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
        print('Mode overwrite ... ')

    elif MODE == 'append':

        print('SQL tables already created.')
        print('Mode append ... ')

    else:

        print('Please choose either mode overwrite either mode append !')

    response = json.loads(requests.get(URL).text)
    for station in response:
        print(station)
        print('-'*30)

        now = datetime.now()
        current_time = now.strftime("%Y/%d/%m %H:%M:%S")

        sql = """ INSERT INTO 
                  stations_info_temp (station_number, station_name, station_adress, contract, latitude, longitude, banking, status, connected, time) 
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        cur = conn.cursor()
        cur.execute(sql, (station["number"], station["name"], station["address"], station["contractName"], station["position"]["latitude"], station["position"]["longitude"], station["banking"], station["status"], station["connected"], current_time))
        conn.commit()