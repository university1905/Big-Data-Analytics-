from kafka import KafkaConsumer
import json
from collections import defaultdict
import re
from pymongo import MongoClient


# Create Kafka consumer
topic = 'topic'
consumer = KafkaConsumer(topic,
                         bootstrap_servers='localhost:9092',
                         group_id='apriori_group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# MongoDB configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['Categories_Wise_Ranking']
collection = db['MyDatabase']

# Dictionary to store data grouped by category
category_data = defaultdict(list)

def extract_category(rank):
    # Extract category from rank
    categories = re.findall(r'(?<=\bin\s).+?(?=\()', rank)
    return categories

def extract_numeric_rank(rank):
    # Regular expression pattern to extract numeric rank
    pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'
    numeric_rank = re.findall(pattern, rank)
    if numeric_rank:
        return int(numeric_rank[0].replace(',', ''))
    else:
        return None

def update_ranking(data):
    # Extract category from rank
    if isinstance(data['rank'], list):
        categories = extract_category(data['rank'][0])
        rank = data['rank'][0]
    else:
        categories = extract_category(data['rank'])
        rank = data['rank']
    
    # Extract numeric rank
    rank_num = extract_numeric_rank(rank)
    
    if rank_num is not None:
        for category in categories:
            # Add data to category dictionary
            category_data[category].append({'title': data['title'], 'rank': rank_num, 'brand': data['brand']})
            # Sort data within each category by rank
            category_data[category] = sorted(category_data[category], key=lambda x: x['rank'])
            # Update MongoDB collection
            collection.update_one({'category': category},
                                  {'$set': {'products': category_data[category]}},
                                  upsert=True)
            # Print the update
            print(f"Category: {category}")
            for item in category_data[category]:
                print(f"Title: {item['title']}, Rank: {item['rank']}, Brand: {item['brand']}")
        print('\n\n\n')
    
    else:
        print("Error: Unable to extract numeric rank.")

# Consume messages from Kafka topic
for message in consumer:
    data = message.value
    update_ranking(data)
