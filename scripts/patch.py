import psycopg2

from connect_sql import config_sql

parameters_sql = config_sql()
conn = psycopg2.connect(**parameters_sql)

print("SQL DataBase connection sucessful !")

command = """
    ALTER TABLE bikes_availability_temp
    RENAME COLUMN time TO time_old;
    ALTER TABLE bikes_availability_temp
    ADD time CHAR(19);
    UPDATE bikes_availability_temp
    SET time = CONCAT(SUBSTRING(time_old, 1, 5), SUBSTRING(time_old, 9, 2), SUBSTRING(time_old, 5, 3), SUBSTRING(time_old, 11, 9));
    ALTER TABLE bikes_availability_temp
    DROP COLUMN time_old;
"""

cur = conn.cursor()
# create table one by one
cur.execute(command)
# close communication with the PostgreSQL database server
cur.close()
# commit the changes
conn.commit()
print('SQL patch done !')