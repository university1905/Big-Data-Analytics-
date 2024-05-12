from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.evaluation import ClusteringEvaluator

# Initialize Spark
spark = SparkSession.builder \
    .appName("kmeans evaluation for Similar Songs") \
    .getOrCreate()

# # Load saved feature_rdd
df = spark.read.parquet('df.parquet')

model = KMeansModel.load('kmeans_model')
predictions = model.transform(df)

# clusterin evaluations
evaluator_silhouette = ClusteringEvaluator(featuresCol= 'features', predictionCol= 'prediction', metricName= 'silhouette')
silhouette_score = evaluator_silhouette.evaluate(predictions)

print("Silhouette Score:", silhouette_score)

spark.stop()