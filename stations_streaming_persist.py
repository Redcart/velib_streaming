import argparse
import psycopg2
from connect_sql import config_sql

if __name__ == '__main__':

    parameters_sql = config_sql()
    conn = psycopg2.connect(**parameters_sql)
    print("SQL DataBase connection sucessful !")
    cur = conn.cursor()

    sql = """
              SELECT * FROM bikes_availability_temp
          """
  
    cur.execute(sql)
    results = cur.fetchall()

    sql = """ INSERT INTO 
              bikes_availability (id, station_number, station_name, station_adress, contract, capacity, nb_available_bikes, nb_available_bike_stands, time) 
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
          """

    for row in results:
        cur.execute(sql, row)

    sql = """
              DELETE FROM bikes_availability_temp
          """

    cur.execute(sql)

    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
    print('SQL table append ! ')

    