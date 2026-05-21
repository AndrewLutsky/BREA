"""
This script assigns a keyword a score per brain region. This results in a
brain_region x keyword matrix.

"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import ast
import tqdm
import numpy as np
import pickle
def process_brain_region_tfidf(brain_region:str,
                               abstracts: list[str],
                               ngram_range = (1, 3)) -> dict[str]:
    """
    This uses tfidf to calculate tfidf scores based on a list of abstracts.
    We then return the relevant words.
    """
    if len(abstracts) == 0:
        return None
    vectorizer = TfidfVectorizer(stop_words = 'english', ngram_range = ngram_range)
    mat = vectorizer.fit_transform(abstracts)
    return mat, vectorizer

def parse_pmids(cell):
    try:
        parsed = ast.literal_eval(cell)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, SyntaxError):
        return []


def top_words(doc_idx, n=10):
    row = X[doc_idx]
    top_idx = row.toarray().argsort()[0][::-1][:n]
    return [(feature_names[i], row[0, i]) for i in top_idx]


def main():
    # Collect the abstracts.
    mouse = pd.read_csv('../Allen/mouse.csv')
    mouse_abstracts = pd.read_csv('../Allen/mouse_abstracts.csv')
    abs_map = dict(zip(mouse_abstracts['PMID'], mouse_abstracts['Abstract']))
    region_data = {}
    for idx in tqdm.tqdm(range(len(mouse))):
        region = mouse['Region'].iloc[idx]
        pmids = parse_pmids(mouse['PMIDs'].iloc[idx])
        corpus_pmids = [int(x) for x in pmids if isinstance(abs_map.get(int(x)), str)]
        corpus = [abs_map[p] for p in corpus_pmids]

        if not corpus:
            continue

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
        mat = vectorizer.fit_transform(corpus)  # (n_docs, n_keywords)

        region_data[region] = {
            'mat': mat,                                    # sparse (n_docs, n_keywords)
            'keywords': vectorizer.get_feature_names_out(),
            'pmids': corpus_pmids
        }

    with open('region_data.pkl', 'wb') as f:
        pickle.dump(region_data, f)

if __name__ == "__main__":
    main()

