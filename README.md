# Music Recommendation System

The project assigned focused on developing a streamlined alternative to Spotify by creating a sophisticated music recommendation and streaming system. This system is designed to assess and implement cutting-edge machine learning algorithms and big data technologies for effective music information retrieval (MIR). The project is structured into several phases: creating an ETL pipeline to process and store features from a large music dataset, utilizing Apache Spark for training a music recommendation model, deploying the model in a Flask-based web application, and using Apache Kafka for real-time music recommendation generation.

## Files

### 1. `preprocess.ipynb`

This piece of code is responsible for the initial preprocessing of the data. It includes loading the Free Music Archive (FMA) dataset, extracting essential audio features using techniques such as Mel-Frequency Cepstral Coefficients (MFCC), and storing these features in a MongoDB database for easy access and manipulation later in the project. It also includes extraction of metadata such as Title, Album, Genre, Date, Path.

### 2. `music_recommendation_system_using_Kmeans.py`

This Python script uses Apache Spark to perform K-means clustering on the preprocessed data stored in MongoDB. The main goal is to group similar songs based on their features to enhance the recommendation process.

### 3. `Kmeans_evaluation.py`

This script evaluates the K-means clustering model implemented in the previous file. It generates evaluation metrics like the silhouette score, which help in assessing the clustering performance and determining the optimal number of clusters.

### 4. `app.py`

This Flask application serves as the frontend of the music recommendation system. It interacts with MongoDB to fetch song data, displays song details, and manages user interactions. The app also integrates Kafka to handle real-time music recommendations based on user activity.

### Additional Files

#### `producer.py`

This script acts as a Kafka producer. It sends song data to a specified Kafka topic whenever a song is played, enabling real-time processing and recommendation.

#### `consumer.py`

Complementing the producer, this Kafka consumer listens for messages (song plays) and triggers the recommendation process based on the current song and user activity. It uses the features and models stored to recommend similar songs.

---

## Execution and Usage

### Setting Up the Environment
1. Ensure Kafka, Spark, Flask and MongoDB services are installed.

### Execution Instructions
1. **Start the Flask app**:  
   Run `python3 app.py` to start the flask app 
2. **Execute the Kafka Consumer**:  
   Run `python3 consumer.py` to start the consumer process that uses the saved kmeans model to generate recommended songs and writes the output to json file.
3. **Activate MongoDB & Open Mongosh**:      Activate Mongo by typing `sudo systemctl start mongod` terminal
   Run Mongosh Terminal by typing `mongosh` in the terminal

---

## Contributors
- **Hamza Burney** || 22i-2058
- **Irtiza Abbas** || 22I-1862
- **Zain Abbas** || 22I-1905



---

