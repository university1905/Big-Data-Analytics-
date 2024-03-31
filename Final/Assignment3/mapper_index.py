#!/usr/bin/env python3

import sys

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




if __name__ == "__main__":
    
    vocabulary, documents = mapper()
    term_frequency = term_frequency_fun(documents, vocabulary)
    idf_frequency = inverse_document_frequency(term_frequency, vocabulary)
    print("Vocabulary;", vocabulary)
    print("term_frequency;", term_frequency)
    print("idf_frequency;", idf_frequency)


