#!/usr/bin/env bash

PROJECT_DIR='/home/redcart/Data_Science/velib_streaming/scripts'
PID_FILE='/home/redcart/Data_Science/velib_streaming/logs/pid_producer.txt'
LOG_FILE='/home/redcart/Data_Science/velib_streaming/logs/resilience_producer.txt'

while true; 

    do

    PID=`cat $PID_FILE`

    if [ -n "$PID" -a -e /proc/$PID ]; then

        true

    else

        cd $PROJECT_DIR && nohup ./stations_producer.py & 
        PID=$!
        echo "$PID" > $PID_FILE
        date=$(date '+%Y-%m-%d %H:%M:%S')
        echo "Kafka producer has been restarted on $date" >> $LOG_FILE
        
    fi
    sleep 30
    done
        
    