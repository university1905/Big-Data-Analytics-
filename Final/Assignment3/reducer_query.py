#!/usr/bin/env python3

import sys
import numpy as np

#query = 'reflects interpretation communism collectivism syndicalism mutualism participatory economics'
def reducer():
    
    # Read input from standard input
    vector_space_retrieval = {}
    vector_space_query = {}

    for line in sys.stdin:

        # Remove leading and trailing whitespace
        line = line.strip()
        data, dict = line.split(';')
        if data == "vector_space_retrieval":
            vector_space_retrieval = eval(dict)
            for key, val in vector_space_retrieval.items():
                vector_space_retrieval[key] = np.array(val)
        elif data == "vector_space_query":
            vector_space_query = eval(dict)
            for key, val in vector_space_query.items():
                vector_space_query[key] = np.array(val)
        
    return vector_space_query, vector_space_retrieval


def scalar_product(vector_space_query, vector_space_retrieval):

    scalar_product = {}
    for doc_id, vectors in vector_space_retrieval.items():
        scalar_product[doc_id] = np.dot(vectors, vector_space_query['query'])
    

    scalar_product_sorted = sorted(scalar_product.items(), key=lambda x: x[1], reverse = True)

    with open("output.txt", 'w') as output_file:
        output_file.write("Rank: \n")
        output_file.write("ID   Title       Relevance_Score\n")
        output_file.write("------------------------------\n")
        for rank, (doc_id, value) in enumerate(scalar_product_sorted[:20], start=1):
            article, title = doc_id.split(" ", 1)
            output_file.write(f"{article:<3}  {title:<10}  {value:.3f}")
            output_file.write("\n")
        result = max(scalar_product, key=scalar_product.get)
        output_file.write(f"\nMost relevant article according to the query: {result}")
    
    print("Rank: \n")
    print("ID   Title       Relevance_Score")
    print("------------------------------")
    for rank, (doc_id, value) in enumerate(scalar_product_sorted[:20], start=1):
        article, title = doc_id.split(" ", 1)
        print(f"{article:<3}  {title:<10}  {value:.3f}")
    
    result = max(scalar_product, key=scalar_product.get)
    print(f"\nMost relevant article according to the query: {result}")

if __name__ == "__main__":

    vector_space_query, vector_space_retrieval = reducer()
    scalar_product(vector_space_query, vector_space_retrieval)
