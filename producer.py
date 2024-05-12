from kafka import KafkaProducer
import json

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


def send_song_data(song_id):
    message = {'song_number': song_id}
    producer.send('topic', value=message)
    print(f"Sent song to topic: {message}")
    producer.flush()