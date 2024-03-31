#!/usr/bin/env python3

import sys
import json

def reducer():

    vocabulary = {}
    term_frequency = {}
    idf_frequency = {}

    # Read input from standard input
    for line in sys.stdin:

        # Remove leading and trailing whitespace
        line = line.strip()
        #print(line)
        data, dict = line.split(';')
        if data == "term_frequency":
            term_frequency = eval(dict)
        elif data == "Vocabulary":
            vocabulary = eval(dict)
        else:
            idf_frequency = eval(dict)
        
    return idf_frequency, term_frequency, vocabulary

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
    
    vector_space = {}

    # Iterate through the TF/Doc_frequency dictionary
    for doc_id, tf_doc_vector in tf_idf_frequency.items():
        vocabulary_array = [0.0]*(vocabulary_size-1)
        for word_id, weight in tf_doc_vector.items():
            # Assign the weight to the corresponding index in the vocabulary array
            vocabulary_array[word_id-1] = weight
        vector_space[doc_id] = vocabulary_array

    return vector_space


if __name__ == "__main__":
    
    idf_frequency, term_frequency, vocabulary = reducer()
    tf_idf_frequency = tf_idf_weights(term_frequency, idf_frequency)
    vocabulary_size = len(vocabulary)
    vector_space = create_vector_space(tf_idf_frequency, vocabulary_size)

    print("Vector_Space;", vector_space)
    print("Vocabulary;", vocabulary)
    print("IDF;", idf_frequency)