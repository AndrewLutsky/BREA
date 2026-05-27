"""
This module contains utils necessary for BREA and its scoring methods.
Author: Andrew Lutsky
Date: 05/27/2026
"""

import pickle
import os
import scipy


def load_pickle(file_path: str) -> tuple[scipy.sparse.spmatrix, list[str], list[str]]:
    """
    Loads the pickle file in question. We expect the pickle file to contain the
    keys ``"matrix"``, ``"regions"``, and ``"keywords"``. If the file is not found we throw
    a ``FileNotFound`` Exception and if the pickle doesn't match the expected schema
    we throw a ``PickleUnloadingException``.

    :param file_path:
        A file path to a schemad pickle file.
    :type file_path: str

    :returns:
        A tuple containing a scipy.sparse.spmatrix, the list of regions
        and the list of keywords.
    :rtype:
        tuple[scipy.sparse.spmatrix, list[str], list[str]]

    :raises FileNotFoundError:
        Raised if the provided file path does not exist.

    :raises PickleUnloadingException:
        Raised if the pickle file does not contain the expected schema.
    """

    # Check if file exists.
    if not os.path.exists(file_path):
        raise FileNotFound()

    # Load the pickle file.
    with open("region_keyword_matrix.pkl", "rb") as f:
        data = pickle.load(f)

    # Try to pull out matrix, regions, and keywords from data, else
    # raise pickle unloading exception.
    try:
        tfidf_matrix = data["matrix"]
        regions = data["regions"]
        keywords = data["keywords"]
    except Exception as e:
        raise PickleUnloadingException() from e

    return (tfidf_matrix, regions, keywords)


class FileNotFound(Exception):
    """
    A simple exception designed to be thrown when the file can't be found.
    """

    def __init__(self):
        super().__init__("File was not found!")


class PickleUnloadingException(Exception):
    """
    An exception aimed at validating the expected pickle schema for the region
    keyword sparse matrix file.

    The function load_pickle expects that the pickle file contains matrix, regions,
    and keywords. These are expected to be scipy.sparse.spmatrix, list[str], and list[str]
    respectively.
    """

    def __init__(self):
        super().__init__(self)
