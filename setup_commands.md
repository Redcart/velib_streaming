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
0 6 * * * python stations_streaming_persistent.py
30 6 * * * python stations_static_info.py --mode append
0 7 * * MON python stations_static_info_persistent.py