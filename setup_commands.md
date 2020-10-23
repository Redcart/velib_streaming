# Download Apache Kafka
wget http://apache.crihan.fr/dist/kafka/0.10.2.1/kafka_2.10-0.10.2.1.tgz
tar xzf kafka_2.10-0.10.2.1.tgz
cd kafka_2.10-0.10.2.1/

# Launch Zookeper Cluster Manager Resources
./bin/zookeeper-server-start.sh ./config/zookeeper.properties

# Launch Kafka broker
./bin/kafka-server-start.sh ./config/server.properties

# Launch python scripts
nohup python script.py &
disown

# cron jobs
crontab -l
crontab -e

# m h  dom mon dow   command
0 6 * * * cd $PROJECT_DIR && ./stations_streaming_persist.py
30 6 * * * cd $PROJECT_DIR && ./stations_static_info.py --mode append
0 7 * * MON cd $PROJECT_DIR && ./stations_static_info_persist.py

# monitoring kafka broker
cd kafka_2.12-2.6.0
./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic velib-stations
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group velib-monitor-stations --describe
./bin/kafka-topics.sh --list --zookeeper localhost:2181

# Increase number of partitions
./bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic velib-stations --partitions 12

# Know how much disk space Kafka uses for storing messages (after they are consumed)
du -sh /tmp/kafka-logs/*

# Change the retention time for messages (here 5 minutes)
bin/kafka-configs.sh --bootstrap-server localhost:2181  --entity-type topics --entity-name velib-stations --alter --add-config retention.ms=300000

# Export SQL table to external csv file (without psql we do not have the rights to do this)
psql bikes_db
\copy (SELECT * FROM bikes_availability) to '/home/redcart/Data_Science/velib_streaming/data/bikes_availability.csv' with csv;
