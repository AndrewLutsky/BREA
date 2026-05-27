""" This experiment was mainly done to determine a knee plot dropoff in tfidf scores. """
import pickle
import numpy
import random
import matplotlib.pyplot as plt

from brea.scoring import grab_top_n_keywords

def main(n_samples: int = 20):
    """ Main fxn
    :param n_samples: Number of samples to randomly pull from without replacement.
    :type n_samples: int

    :returns None
    """

    with open("../../data/scripts/region_keyword_matrix.pkl", "rb") as f:
        data = pickle.load(f)
    
    # Access contents
    tfidf_matrix = data["matrix"]
    regions = data["regions"]
    keywords = data["keywords"]
    vectorizer = data["vectorizer"]
    

    # Sample ~20 random indices
    sampled_idxs = random.sample(range(0, len(regions)), n_samples)
    sampled_regions = [regions[i] for i in sampled_idxs]

    # Let us grab the scores from these regions up to 100 words. 
    print(sampled_regions)

    vectors = [tfidf_matrix[i] for i in sampled_idxs]
    keys = [keywords[i] for i in sampled_idxs]
    print(len(vectors), len(keys))
    vectors = [grab_top_n_keywords(i, keywords) for i in vectors]
    
    values = [[i[1] for i in vector] for vector in vectors]

    # PLOTTING
    plt.figure(figsize=(10,10))
    boxplot_data = list(zip(*values))
    plt.boxplot(boxplot_data)
    plt.xlabel("Keyword Rank Index")
    plt.ylabel("TF-IDF Value")
    plt.title(f"Elbow Plot of TFIDF Values(n = {n_samples})")
    plt.savefig("TFIDF_Scores.png")
    return 


if __name__ == "__main__":
    main()

