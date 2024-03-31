# Naïve Search Engine Utilising MapReduce Technology:

This repository contains code files for a Search Engine that utilizes Apache Hadoop's MapReduce technology to allow users to find desired documents against a query, as part of an assignment for the Fundamental of Big Data Analytics (DS2004) course.

### Dependencies:

* Jupyter Notebook ([install](https://docs.jupyter.org/en/latest/install.html))
* pandas ([install](https://pandas.pydata.org/docs/getting_started/install.html))
* NumPy ([install](https://numpy.org/install/))

## Introduction:


The objective of this project is to develop a basic search engine using the MapReduce paradigm. Search engines have played a pioneering role in addressing the challenge of handling vast amounts of data while maintaining low-latency responses. Consider an average search engine with millions of indexed documents. It must swiftly process hundreds to thousands of queries per second and deliver a list of the most relevant documents in under a millisecond.

The challenge of locating relevant information stands as a critical issue within the realm of information retrieval, comprising two interconnected tasks:

Document Indexing: This task involves creating an index of the documents to facilitate quick retrieval of relevant documents based on search queries.

Query Processing: The task of processing user queries and retrieving the most relevant documents from the index. This task prioritizes swift response times.

While query processing prioritizes swift response times, indexing can be accomplished offline and aligns more closely with the concept of batch processing. Hadoop’s MapReduce framework offers a viable solution for indexing extensive text corpora that exceed the capacity of a single machine.

## Usage:

* ``Music Recommendation Based on Rhythmic Similarity Using Locality-Sensitive Hashing (LSH).ipynb`` — Contains the implementation of our Locality-Sensitive Hashing (LSH) implementation to train and evaluate a music recommendation system on the audio dataset.
* ``app.py`` — Source code for the web application (Flask) that accompanies the music recommendation system.
* ``templates`` — Contains the source codes for the web pages, namely ``index.html`` and ``predict.html``, which are rendered by the web application (Flask).
* ``static`` — Contains all the icons and visual elements utilised by the web application (Flask).
* ``static\files`` — Directory where the audio files uploaded by users on the web application (Flask) are stored.
* ``features.pkl`` — Object file that contains the Mel-Frequency Cepstral Coefficients (MFCC) features of all the audio files utilised for training.
* ``music.ann`` — Memory-mapped (mmap) file that contains the AnnoyIndex object for the music recommendation system utilising Approximate Nearest Neighbors (ANN).

## Instructions (Execution):

* Execute the ``app.py`` file and access the given link to the host port.
* Upload any audio file into the system.
* Once you reach the ``/predict`` page, you will receive both the best and worst recommendations for the uploaded audio file.
* Additionally, a file named ``pied_piper_download.csv`` will be saved in the current directory, which will include similar audio segments identified from the uploaded audio file.

## Contributors:

This project exists thanks to the extraordinary people who contributed to it.
* **[Hamza Mahmood Burney]((https://github.com/HamzaBurney)) (i222058@nu.edu.pk)**
* **[Irtiza Abbas]((https://github.com/irtizaab)) (i221862@nu.edu.pk)**
* **[Zain Abbas](https://github.com/ZainAbbas97) (i221905@nu.edu.pk)**

---
