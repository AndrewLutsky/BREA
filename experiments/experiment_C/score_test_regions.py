""" This experiment was mainly done to determine a knee plot dropoff in tfidf scores. """
import pickle
import numpy
import random
import matplotlib.pyplot as plt
import pandas as pd
from brea.scoring import grab_top_n_keywords

def main(regions_allen: list[str]):
    """ Main fxn
    :param regions_allen: list of Allen Brain Atlas regions.
    :type regions_allen: list[str]

    :returns None
    """

    with open("../../data/scripts/region_keyword_matrix.pkl", "rb") as f:
        data = pickle.load(f)
    
    # Access contents
    tfidf_matrix = data["matrix"]
    regions = data["regions"]
    keywords = data["keywords"]
    vectorizer = data["vectorizer"]
    

    # Load in regions 
    idxs = []
    try:
        for x in regions_allen:
            idxs.append(regions.index(x))
    except:
        pass

    vectors = [tfidf_matrix[i] for i in idxs]
    keys = [keywords[i] for i in idxs]
    vectors = [grab_top_n_keywords(i, keywords, n = 200) for i in vectors]
    print(vectors)
    


if __name__ == "__main__":

    df = pd.read_csv("benchmark_c_2.csv", sep = "\t")['Region']
    main(df)

