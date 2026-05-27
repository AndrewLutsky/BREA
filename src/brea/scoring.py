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
        

    def calculate_overlap_score(regions: list[str],
                                n: int = 50): 


def overlap_score_brain_regions(
    tfidf_mat: scipy.sparse.spmatrix,
    regions: list[str],
    keywords: list[str],
    n: int = 50,
) -> dict[str,]:
    """
    Score brain regions using a TF-IDF keyword representation.

    This function evaluates each brain region based on the TF-IDF
    representation of its associated keywords. Typically, the function
    extracts the top-N weighted keywords per region and computes a
    region-level score or ranking for downstream analysis and comparison.

    :param tfidf_mat:
        Sparse TF-IDF matrix of shape ``(n_regions, n_keywords)``,
        where each row corresponds to a brain region and each column
        corresponds to a keyword feature.
    :type tfidf_mat: scipy.sparse.spmatrix

    :param regions:
        List of brain region names corresponding to the rows of
        ``tfidf_mat``.
    :type regions: list[str]

    :param keywords:
        List of keyword strings corresponding to the columns of
        ``tfidf_mat``.
    :type keywords: list[str]

    :param n:
        Number of top keywords to consider per region.
    :type n: int

    :returns:
        Region scoring results. The exact structure depends on the
        implemented scoring strategy.
    :rtype:
        Any
    """

    # TODO
    pass
