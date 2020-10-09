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
