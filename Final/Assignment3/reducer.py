#!/usr/bin/env python3

import sys
import numpy as np

query = 'reflects interpretation communism collectivism syndicalism mutualism participatory economics'
def reducer():
    # Read input from standard input
    vector_space_retrieval = {}
    vocabulary = {}
    idf_frequency = {}
    for line in sys.stdin:
        # Remove leading and trailing whitespace
        
        line = line.strip()
        #print(line)
        data, dict = line.split(';')
        if data == "Vector_Space":
            vector_space_retrieval = eval(dict)
            for key, val in vector_space_retrieval.items():
                vector_space_retrieval[key] = np.array(val)
        elif data == "Vocabulary":
            vocabulary = eval(dict)
        else:
            idf_frequency = eval(dict)
        
    return idf_frequency, vector_space_retrieval, vocabulary

def term_frequency_fun(vocabulary, query):

    term_frequency = {}
    # Calculate term frequency for each document
        
    tf_vector = {word_id: 0 for word_id in vocabulary.values()}
    # Split document into words
    words = query.lower().split()
    # Count term frequency for each word
    for word in words:
        
        if word in vocabulary:
            word_id = vocabulary[word]
            tf_vector[word_id] += 1
    # Store term frequency vector for current document
    term_frequency["query"] = tf_vector

    return term_frequency

def tf_idf_weights(term_frequency, idf_frequency):
    
    tf_idf_frequency = {}
    for doc_id, tf_vector in term_frequency.items():
        tf_doc_vector = {}
        for word_id, tf in tf_vector.items():
            if idf_frequency[word_id] > 0:
                tf_doc_vector[word_id] = tf / idf_frequency[word_id]
            else:
                tf_doc_vector[word_id] = 0
        tf_idf_frequency[doc_id] = tf_doc_vector

    return tf_idf_frequency

def create_vector_space(tf_idf_frequency, vocabulary_size):
    # Initialize a NumPy array of zeros with the given vocabulary size
    vector_space = {}
    

    # Iterate through the TF/Doc_frequency dictionary
    for doc_id, tf_doc_vector in tf_idf_frequency.items():
        vocabulary_array = [0.0]*(vocabulary_size-1)
        for word_id, weight in tf_doc_vector.items():
            # Assign the weight to the corresponding index in the vocabulary array
            vocabulary_array[word_id-1] = weight
        vector_space[doc_id] = vocabulary_array

    return vector_space

def scalar_product(vector_space_query, vector_space_retrieval):

    scalar_product = {}
    for doc_id, vectors in vector_space_retrieval.items():
        scalar_product[doc_id] = np.dot(vectors, vector_space_query['query'])
    

    scalar_product_sorted = sorted(scalar_product.items(), key=lambda x: x[1], reverse = True)

    print("Rank: \n")
    print("ID   Title       Relevance_Score")
    print("------------------------------")
    for rank, (doc_id, value) in enumerate(scalar_product_sorted[:20], start=1):
        article, title = doc_id.split(" ", 1)
        print(f"{article:<3}  {title:<10}  {value:.3f}")
    
    result = max(scalar_product, key=scalar_product.get)
    print(f"\nMost relevant article according to the query: {result}")


if __name__ == "__main__":

    idf_frequency, vector_space_retrieval, vocabulary = reducer()
    term_frequency = term_frequency_fun(vocabulary, query)
    tf_idf_frequency = tf_idf_weights(term_frequency, idf_frequency)
    vocabulary_size = len(vocabulary)
    vector_space_query = create_vector_space(tf_idf_frequency, vocabulary_size)
    for key, val in vector_space_query.items():
        vector_space_query[key] = np.array(val)
    
    scalar_product(vector_space_query, vector_space_retrieval)
