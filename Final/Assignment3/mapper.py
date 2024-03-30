#!/usr/bin/env python3

import sys
import numpy as np

def mapper():

    vocabulary = {}
    documents = {}
    # Read input from standard input
    for line in sys.stdin:
        # Remove leading and trailing whitespace
        line = line.strip()
        if len(line) == 0: #skip the empty line
            continue
        #key, value = line.split(',')  # Split only at the first comma
        if(len(line.split(',')) == 3):
            Article_ID, Title, Text = line.split(',')
            documents[Article_ID + " " + Title] = Text.strip()  # Remove leading/trailing whitespace from value
        else:
            word, word_ID = line.split(',')
            vocabulary[word.strip()] = int(word_ID)  # Remove leading/trailing whitespace from key
        
        
    return vocabulary, documents


def term_frequency_fun(documents, vocabulary):

    term_frequency = {}
    # Calculate term frequency for each document
    for doc_id, content in documents.items():
        # Initialize term frequency vector for current document
        tf_vector = {word_id: 0 for word_id in vocabulary.values()}
        # Split document into words
        words = content.lower().split()
        # Count term frequency for each word
        for word in words:
            if word in vocabulary:
                word_id = vocabulary[word]
                tf_vector[word_id] += 1
        # Store term frequency vector for current document
        term_frequency[doc_id] = tf_vector

    return term_frequency

def inverse_document_frequency(term_frequency, vocabulary):
    # Calculate document frequency for each term
    idf_frequency = {word_id: sum(1 for tf_vector in term_frequency.values() if tf_vector[word_id] > 0) for word_id in vocabulary.values()}
    return idf_frequency

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
    
    vocabulary, documents = mapper()
    term_frequency = term_frequency_fun(documents, vocabulary)
    idf_frequency = inverse_document_frequency(term_frequency, vocabulary)
    tf_idf_frequency = tf_idf_weights(term_frequency, idf_frequency)
    vocabulary_size = len(vocabulary)
    vector_space = create_vector_space(tf_idf_frequency, vocabulary_size)
    print("Vector_Space;", vector_space)
    print("Vocabulary;", vocabulary)
    print("IDF;", idf_frequency)


