import json
from kafka import KafkaProducer
import time

# Configure Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'topic'

# Path to your JSON file
file_path = 'dataset.json'

# Read data from the file and send each dictionary to Kafka topic
with open(file_path, 'r') as file:
    for line in file:
        try:
            # Parse JSON from each line
            data = json.loads(line)
            # Send the JSON data to Kafka topic
            producer.send(topic, json.dumps(data).encode('utf-8'))
            print(f"Data sent to topic: {data}")
            time.sleep(1)  
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            continue

# Close the producer
producer.close()
