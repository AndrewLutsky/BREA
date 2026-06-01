"""
Builds a brain_region x keyword matrix using a single TF-IDF vectorizer
fitted over all regions, where each region is represented as one document
(all its abstracts concatenated). This ensures IDF is shared across regions,
making scores comparable for enrichment analysis.
"""
import numpy as np
import pandas as pd
import pickle
import ast
import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer


def parse_pmids(cell):
    try:
        parsed = ast.literal_eval(cell)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, SyntaxError):
        return []


def build_region_corpus(mouse: pd.DataFrame, abs_map: dict) -> tuple[list[str], list[str]]:
    """
    For each brain region, concatenate all its abstracts into a single document.
    Returns (region_names, region_documents).
    """
    regions = []
    documents = []

    for idx in tqdm.tqdm(range(len(mouse))):
        region = mouse['Region'].iloc[idx]
        pmids = parse_pmids(mouse['PMIDs'].iloc[idx])
        corpus_pmids = [int(x) for x in pmids if isinstance(abs_map.get(int(x)), str)]
        abstracts = [abs_map[p] for p in corpus_pmids][:100]

        if not abstracts:
            continue

        # Concatenate all abstracts for this region into one document
        regions.append(region)
        documents.append(" ".join(abstracts))

    return regions, documents


def main():
    mouse = pd.read_csv('../Allen/mouse.csv')
    mouse_abstracts = pd.read_csv('../Allen/mouse_abstracts.csv')
    abs_map = dict(zip(mouse_abstracts['PMID'], mouse_abstracts['Abstract']))

    print("Building per-region documents...")
    regions, documents = build_region_corpus(mouse, abs_map)
    print(f"  {len(regions)} regions with abstracts.")

    # Fit a single TF-IDF vectorizer over all region-documents.
    # - TF:  term frequency within this region's concatenated abstracts
    # - IDF: penalises terms that appear across many regions (non-specific)
    # sublinear_tf dampens the effect of a term appearing 100x vs 10x,
    # which matters when regions with many abstracts dominate raw counts.
    print("Fitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1,2),
        sublinear_tf=True,      # replace tf with 1 + log(tf)
        min_df=2,               # ignore terms that appear in only 1 region
    )
    tfidf_matrix = vectorizer.fit_transform(documents)  # (n_regions, n_keywords)
    keywords = vectorizer.get_feature_names_out()

    print(f"  Matrix shape: {tfidf_matrix.shape}  (regions × keywords)")

    # Convert to DataFrame for easy inspection / downstream use
    df = pd.DataFrame.sparse.from_spmatrix(
        tfidf_matrix,
        index=regions,
        columns=keywords,
    )

    # --- quick sanity check: top keywords per region ---
    print("\nTop 10 keywords for first 3 regions:")
    dense = tfidf_matrix.toarray()
    for i, region in enumerate(regions[:3]):
        top_idx = dense[i].argsort()[::-1][:10]
        top = [(keywords[j], round(dense[i, j], 4)) for j in top_idx]
        print(f"  {region}: {top}")

    ## Save outputs
    #df.to_csv('region_keyword_matrix.csv', index=False)
    #print("\nSaved region_keyword_matrix.csv")

    # Also save the vectorizer and sparse matrix for downstream enrichment
    with open("region_keyword_matrix.pkl", "wb") as f:
        pickle.dump({
            "matrix": tfidf_matrix,          # scipy sparse (n_regions, n_keywords)
            "regions": regions,
            "keywords": keywords.tolist(),
            "vectorizer": vectorizer,
        }, f)
    print("Saved region_keyword_matrix.pkl")


if __name__ == "__main__":
    main()
