from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeansModel
from scipy.spatial.distance import cosine

# Initialize Spark
spark = SparkSession.builder \
    .appName("Query kmeans for Similar Songs") \
    .getOrCreate()

# # Load saved feature_rdd
feature_rdd = spark.sparkContext.pickleFile("feature_rdd.pickle")
df = spark.read.parquet('df.parquet')

model = KMeansModel.load('kmeans_model')
predictions = model.transform(df)

def recommend_top_songs(song_number, predictions, input_song_features,top_n = 5):
    # Find the cluster assigned to the given song
    cluster = predictions.filter(predictions['Label'] == song_number).select('prediction').collect()[0]['prediction']
    
    # Get other songs belonging to the same cluster
    recommended_songs = predictions.filter(predictions['prediction'] == cluster).select('Label', 'Features').collect()
    
    # # Filter out the input song from the recommendations
    recommended_songs = [(song['Label'], song['Features']) for song in recommended_songs if song['Label'] != song_number]
    
    # Calculate similarity scores between the input song and recommended songs
    similarity_scores = []
    print('\n\n\n', input_song_features, '\n\n\n')
    for recommended_song_id, recommended_song_features in recommended_songs:
        similarity_score = cosine(input_song_features, recommended_song_features)
        similarity_scores.append((recommended_song_id, similarity_score))
    
    # Sort recommended songs based on similarity scores
    ranked_recommendations = sorted(similarity_scores, key=lambda x: x[1])
    
    # Return the top N recommended songs
    top_recommendations = [song_id for song_id, _ in ranked_recommendations[:top_n]]

    return top_recommendations



song_number = 5
similar_songs = recommend_top_songs(song_number, predictions, feature_rdd.lookup(song_number)[0])
print("Recommended similar songs for song {}: {}".format(song_number, similar_songs))

# Stop Spark
spark.stop()
