from kafka import KafkaConsumer
from collections import defaultdict
from itertools import combinations
from pymongo import MongoClient

# Setup MongoDB Connection
client = MongoClient('localhost', 27017)
db = client.mydatabase
collection = db.frequent_itemsets

def parse_product_names(message):
    try:
        data = eval(message)
        product_names = data.get('also_buy', [])
        return product_names.split() if isinstance(product_names, str) else product_names
    except Exception as e:
        print(f"Error parsing message: {e}")
        return []

def generateCandidates(items, k):
    """ Generate k-item candidates from (k-1)-item frequent itemsets. """
    return set([
        frozenset(i.union(j)) for i in items for j in items if len(i.union(j)) == k
    ])

def pcyAlgo(transactions, minSupport):
    allLevels = []
    itemCount = defaultdict(int)
    for transaction in transactions:      # Increment count for each item in the transaction
        for item in transaction:
            itemCount[item] += 1
    
    currentLevel = {item for item, count in itemCount.items() if count >= minSupport}
    allLevels.append(currentLevel)

    itemCount = defaultdict(int)
    for transaction in transactions:
        for item in combinations(transaction, 2):  # Start directly with pairs
            itemCount[frozenset(item)] += 1

    # Initial frequent itemsets (starting with pairs)
    currentLevel = {item for item, count in itemCount.items() if count >= minSupport}
    allLevels.append(currentLevel)

    k = 3
    while currentLevel:

        # Generate candidates of size k from currentLevel of size k-1
        candidates = generateCandidates(currentLevel, k)
        if not candidates:
            break
        candidateCount = defaultdict(int)

        for transaction in transactions:
            transactionSet = frozenset(transaction)
            for candidate in candidates:
                if candidate <= transactionSet:
                    candidateCount[candidate] += 1

        # Filter by minimum support and update currentLevel
        currentLevel = {itemset for itemset, count in candidateCount.items() if count >= minSupport}
        if currentLevel:
            allLevels.append(currentLevel)
        k += 1

    return allLevels

def printFrequentItemSets(itemSets):
    for level, sets in enumerate(itemSets, start=1):
        item_list = []
        for itemset in sets:
            if level > 1:
                item_list.append(','.join(map(str, itemset)))
            else:
                item_list.append(itemset)
        # Store the complete list of itemsets of the same length in one document
        document = {
            'lengthOfArray': level,
            'itemset': item_list,
            'count': len(item_list)
        }
        collection.insert_one(document)
        print(f"Frequent itemsets of length {level}:", item_list)

# Main processing loop

topic = 'topic'
consumer = KafkaConsumer(topic,
                         bootstrap_servers='localhost:9092',
                         group_id='apriori_group',
                         auto_offset_reset='earliest')

window_size = 100
window = []
minSupport = 2

try:
    for message in consumer:
        product_names = parse_product_names(message.value.decode('utf-8'))
        if product_names:
            window.append(product_names)
            if len(window) > window_size:
                window.pop(0)
            if len(window) == window_size:    
                allFrequentItemSets = pcyAlgo(window, minSupport)  # Generate up to 20-itemsets
                printFrequentItemSets(allFrequentItemSets)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
