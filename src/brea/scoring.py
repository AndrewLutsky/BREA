"""
This module contains the logic for scoring lists of brain regions
Author: Andrew Lutsky
Date: 05/25/2026
"""

import numpy as np
import scipy
from brea.utils import load_pickle

def grab_top_n_keywords(
    row: scipy.sparse.spmatrix, keywords: list[str], n: int = 50
) -> list[tuple[str, float]]:
    """
    Retrieve the top-N keywords from a sparse TF-IDF row.

    This function extracts the nonzero entries from a sparse matrix row,
    sorts them in descending order by TF-IDF score, and returns the
    corresponding keyword-score pairs.

    :param row:
        A sparse matrix row containing TF-IDF values.
    :type row: scipy.sparse.spmatrix

    :param keywords:
        List of keyword strings corresponding to matrix column indices.
    :type keywords: list[str]

    :param n:
        Number of top keywords to return.
    :type n: int

    :returns:
        A list of ``(keyword, score)`` tuples sorted by descending score.
    :rtype: list[tuple[str, float]]
    """
    # Extract nonzero sparse entries.
    indices = row.indices
    values = row.data

    # Sort indices by descending TF-IDF score.
    order = np.argsort(values)[::-1][:n]

    # Construct keyword-score pairs.
    top_keywords = [(keywords[indices[i]], float(values[i])) for i in order]

    return top_keywords


class ScoringModule:
    def __init__(self, pickle_file: str) -> None:
        """
        Initializes the Scoring module and stores the tfidf, regions, and keywords
        within the scoring object
        """
        self.pickle_file = pickle_file
        self.mat, self.regions, self.keywords = load_pickle(self.pickle_file)
         

    def calculate_overlap_score(self,
                                regions: list[str],
                                n: int = 50,
                                multi_set = True
    ) -> dict[str, list[str]]: 
        """
        Creates a dictionary mapping regions to top n keywords.
        """
        region_dic = {}
        for region in regions:
            row = self.regions.index(region) 
            region_dic[region] = grab_top_n_keywords(self.mat[row], self.keywords, n) 

        # Find score across different regions
        
        # Create set of keywords
        keyword_set = set()
        for _, val in region_dic.values():
            for x in val:
                keyword_set.add(x)
        
        # Iterate through keywords and find frac occurence.
        score_dic = {}
        for keyword in keyword_set:
            count = sum(1 for val in region_dic.values() if keyword in val)
            if not multi_set or count > 1:
                score_dic[keyword] = count / tot
        return score_dic


