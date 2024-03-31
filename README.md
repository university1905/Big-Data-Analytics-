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

* ``Text_Preprocessing.ipynb`` — Contains the implementation of our text preprocessing implementation to extract only useful information from the dataset.
* ``dataset.txt`` — The TextPreprocessing.ipynb file will make dataset.txt file that will be fed into the Mapper.
* ``mapper_index.py`` — Contains the codes for calculating the Term Frequency and Inverse Document Frequency and utilizes the ``dataset.txt`` file.
* ``reducer_index.py`` — This calculates the weights and the vector space from the output of ```mapper_index.py```
* ``mapper_query.py`` — Reading the query, and Vector Space, IDF and Vocabulary of the original dataset. Then term frequence, IDF the weights and the Vector Space for the query are generated.
* ``reducer_query.py`` — Calculates the scalar product of both Vector Spaces and displays the output in the ``output.txt file``

## Instructions (Execution):
* Step 1:
  Run all the cells of the jupyter file
  This would create a dataset.txt.
  In dataset.txt, we have created a new dataset after preprocessing at, as well as        vocabulary creation

* Step 2:
  - hadoop fs -mkdir -p /input/
  Create a folder named 'input' in Hadoop

*  Step 3:
  - hadoop fs -put dataset.txt /input/dataset.txt  
  Insert the dataset.txt which was craeted in step 1, into the 'input' folder.

*  Step 4:
  - hadoop jar /usr/local/hadoop-2.10.2/share/hadoop/tools/lib/hadoop-streaming-          2.10.2.jar -input /input/dataset.txt -output /input/output1 -mapper mapper_index.py -   reducer reducer_index.py -file mapper_index.py -file reducer_index.py

  Run the above script for indexing. This would create an output file which has the       location: /input/output1/part-00000

*  Step 5:
  - hadoop jar /usr/local/hadoop-2.10.2/share/hadoop/tools/lib/hadoop-streaming-          2.10.2.jar -input /input/output1/part-00000 -output /input/output2 -mapper             "mapper_query.py 'your query'" -reducer reducer_query.py -file mapper_query.py -file     reducer_query.py

  Change the 'your query' part with your specific query

  Run the above script for query results. This would create an output file named         output.txt in the local folder, which contains the final results of the query :)


## Contributors:

This project exists thanks to the extraordinary people who contributed to it.
* **[Hamza Mahmood Burney](https://github.com/HamzaBurney) (i222058@nu.edu.pk)**
* **[Irtiza Abbas](https://github.com/irtizaab) (i221862@nu.edu.pk)**
* **[Zain Abbas](https://github.com/ZainAbbas97) (i221905@nu.edu.pk)**

---
