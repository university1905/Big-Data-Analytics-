from kafka import KafkaConsumer
import json
from pyspark.ml.clustering import KMeansModel
from scipy.spatial.distance import cosine
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("Query Annoy Index for Similar Songs") \
    .getOrCreate()

# Load saved feature_rdd
feature_rdd = spark.sparkContext.pickleFile("feature_rdd.pickle")
df = spark.read.parquet('df.parquet')

model = KMeansModel.load('kmeans_model')
predictions = model.transform(df)

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'topic',
    bootstrap_servers=['localhost:9092'],
    # auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def get_similar_songs_path(song_number, similar_song_numbers):
    similar_songs_paths = []
    for number in similar_song_numbers:
        if song_number ==number:
            continue
        # Filter the RDD to find the record(s) with the matching number
        matching_record = feature_rdd.filter(lambda x: x[0] == number)
        matching_record = matching_record.first()
        corresponding_path = matching_record[2]
        similar_songs_paths.append(corresponding_path)
    
    return similar_songs_paths

def recommend_top_songs(song_number, predictions, input_song_features,top_n = 10):
    # Find the cluster assigned to the given song
    cluster = predictions.filter(predictions['Label'] == song_number).select('prediction').collect()[0]['prediction']
    
    # Get other songs belonging to the same cluster
    recommended_songs = predictions.filter(predictions['prediction'] == cluster).select('Label', 'Features').collect()
    
    # # Filter out the input song from the recommendations
    recommended_songs = [(song['Label'], song['Features']) for song in recommended_songs if song['Label'] != song_number]
    
    # Calculate similarity scores between the input song and recommended songs
    similarity_scores = []
    for recommended_song_id, recommended_song_features in recommended_songs:
        similarity_score = cosine(input_song_features, recommended_song_features)
        similarity_scores.append((recommended_song_id, similarity_score))
    
    # Sort recommended songs based on similarity scores
    ranked_recommendations = sorted(similarity_scores, key=lambda x: x[1])
    
    # Return the top N recommended songs
    top_recommendations = [song_id for song_id, _ in ranked_recommendations[:top_n]]

    return top_recommendations


for message in consumer:
    print("Consumer started running")
    message_data = message.value
    song_number = message_data['song_number']
    print(f"Received song for processing: {song_number}")

    song_features = feature_rdd.lookup(song_number)[0]
    similar_song_numbers = recommend_top_songs(song_number, predictions, feature_rdd.lookup(song_number)[0])
    similar_songs_path = get_similar_songs_path(song_number, similar_song_numbers)

    similar_songs = {'song_id': song_number, 'path': similar_songs_path}
    print(similar_songs)
    with open('recommended_songs.json', 'w') as json_file:
        json.dump(similar_songs, json_file)
