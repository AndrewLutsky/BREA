"""
This module is primarily to run entrez queries.
Author: Andrew Lutsky
Date: 05/27/2026
"""

from Bio import Entrez


def retrieve_pmids(
    keyword: str, additional_operators: list[str], api_key: str
) -> list[str]:
    """
    This retrieves pmids based off of a keyword
    and additional operators.
    :param keyword: A keyword to search for pubmed for.
    :type keyword: str
    :param additional_operators: Additional terms to search for with the keyword.
    :type additional_operators: list[str]
    :param api_key: Api key to be used for entrez.
    :type api_key: str
    :returns list[str]
    """
    Entrez.api_key = api_key

    terms = [keyword] + additional_operators
    query = " AND ".join(terms)
    print(f"Query: {repr(query)}")
    with Entrez.esearch(db="pubmed", term=query, retmax=100000) as handle:
        record = Entrez.read(handle)

    return record["IdList"]
