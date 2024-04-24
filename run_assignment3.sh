#!/bin/bash

# Open a new terminal window and run Zookeeper server
gnome-terminal -- bash -c "cd kafka && bin/zookeeper-server-start.sh config/zookeeper.properties"

# Wait for 2 seconds before opening the next terminal window
sleep 5

# Open a new terminal window and run Kafka server
gnome-terminal -- bash -c "cd kafka && bin/kafka-server-start.sh config/server.properties"


# Wait for 15 seconds before opening the next terminal window
sleep 15

# Function to launch consumer script and wait for it to finish
launch_consumer() {
    gnome-terminal -- bash -c "cd BigData/Assignment3 && python3 $1; read -p 'Press Enter to close'"
    wait $!
}

# Open a new terminal window and delete topic
gnome-terminal -- bash -c "cd kafka && kafka-topics.sh --delete --topic topic --bootstrap-server localhost:9092" &
wait $!

# Wait for 2 seconds before opening the next terminal window
sleep 2

# Open a new terminal window and create new topic
gnome-terminal -- bash -c "cd kafka && bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic" &
wait $!

# Wait for 2 seconds before opening the next terminal window
sleep 2

# Launch consumers one by one
launch_consumer custom.py &
wait $!

launch_consumer apriori.py &
wait $!

launch_consumer pcy.py &
wait $!

# Wait for 4 seconds before opening the next terminal window
sleep 4

# Open a new terminal window and run the Python producer
gnome-terminal -- bash -c "cd BigData/Assignment3 && python3 producer.py; read -p 'Press Enter to close'"

