from kafka import KafkaConsumer
import itertools
from pymongo import MongoClient

# Function to parse product names from the message
def parse_product_names(message):
    try:
        data = eval(message)  
        product_names = data.get('also_buy', [])
        return product_names.split() if isinstance(product_names, str) else product_names
    except Exception as e:
        print(f"Error parsing message: {e}")
        return []

# Function to generate candidate itemsets of size k
def generate_candidate_itemsets(itemsets, k):
    if any(isinstance(item, (tuple, list)) for item in itemsets):
        itemsets = [item for sublist in itemsets for item in sublist]
    itemsets = set(itemsets)
    return [subset for subset in itertools.combinations(itemsets, k)]

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client.mydatabase
collection = db.apriori

if __name__ == "__main__":
    topic = 'topic'
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id='apriori_group', auto_offset_reset='earliest')
    window_size = 100
    window = []
    min_support = 2

    try:
        for message in consumer:
            product_names = parse_product_names(message.value.decode('utf-8'))
            if product_names:
                window.append(product_names)
                if len(window) > window_size:
                    window.pop(0)
                if len(window) == window_size:    
                    # Start with k=2 for pairs
                    k = 2
                    item_counts = {}

                    # Generate candidate itemsets of size 2 initially
                    candidate_itemsets = generate_candidate_itemsets([item for sublist in window for item in sublist], k)
                    for transaction in window:
                        for pair in candidate_itemsets:
                            if all(item in transaction for item in pair):
                                item_counts[pair] = item_counts.get(pair, 0) + 1

                    # Store and print frequent itemsets of size 2 or more
                    while candidate_itemsets:
                        frequent_itemsets = [pair for pair, count in item_counts.items() if count >= min_support]
                        if frequent_itemsets:
                            collection.insert_one({'length': k, 'itemsets': [' '.join(pair) for pair in frequent_itemsets], 'counts': [item_counts[pair] for pair in frequent_itemsets]})
                            # Generate candidates for next higher size
                            k += 1
                            candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, k)
                            item_counts = {}
                            for transaction in window:
                                for pair in candidate_itemsets:
                                    if all(item in transaction for item in pair):
                                        item_counts[pair] = item_counts.get(pair, 0) + 1
                        else:
                            break
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()