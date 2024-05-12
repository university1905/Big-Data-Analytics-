from pyspark.sql import SparkSession
import pymongo
import pandas as pd
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType
from pyspark.sql.functions import substring
from pyspark.sql.functions import udf
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.clustering import KMeans

# Initialize Spark
spark = SparkSession \
    .builder \
    .appName("Music Recommendation Model") \
    .getOrCreate()

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["BDA_Project"]
collection = db["songs_data"]

# Retrieve data from the collection
cursor = collection.find()

# Convert the data to a Pandas DataFrame
df_pandas = pd.DataFrame(list(cursor))
# Drop the _id field from the DataFrame
df_pandas = df_pandas.drop(columns=['_id'])
# Convert the array elements to floating-point values
df_pandas["feature"] = df_pandas["feature"].apply(lambda x: [float(i) for i in x])

# Define the schema for the Spark DataFrame
schema = StructType([
    StructField("feature", ArrayType(FloatType()), True),
    StructField("path", StringType(), True), 
])

df = spark.createDataFrame(df_pandas, schema = schema)

array_to_vector_udf = udf(lambda arr: Vectors.dense(arr), VectorUDT())
df = df.select(array_to_vector_udf(df['feature']).alias('features'), df['path'])

# Extract the number from the "path" column
df = df.withColumn("label", substring("path", 15, 6))

# Convert the "number" column to integer type
df = df.withColumn("label", df["label"].cast("int"))

kmeans = KMeans(featuresCol = "features", k = 10, seed = 1)
model = kmeans.fit(df)

predictions = model.transform(df)

feature_rdd = df.select("label", "features", "path").rdd.map(lambda x: (x[0], x[1], x[2]))
model.save('kmeans_model')

# Save feature_rdd locally
feature_rdd.saveAsPickleFile("feature_rdd.pickle")
df.write.parquet('df.parquet')

# Stop Spark session
spark.stop()
