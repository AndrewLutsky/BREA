""" This scripts just collects all pmids and locally stores all of the results."""
from brea.entrez import retrieve_pmids
import pandas as pd
import json
import Bio.Entrez
import ast
import time
import xml.etree.ElementTree as ET
import tqdm
def main():
    # Read in human and mouse data.
    mouse = pd.read_csv("../Allen/mouse.csv")
    human = pd.read_csv("../Allen/human.csv")
    with open("config.json", 'r') as f:
        config = json.load(f)
        Bio.Entrez.email = config['ENTREZ_EMAIL']
        f.close()
    # PMIDs

    def parse_pmids(cell):
        try:
            parsed = ast.literal_eval(cell)
            return parsed if isinstance(parsed, list) else []
        except (ValueError, SyntaxError):
            return []

    def parse_xml_abstracts(xml_text: str) -> list[dict]:
        rows = []
        root = ET.fromstring(xml_text)
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID", default="")
            title = article.findtext(".//ArticleTitle", default="")
            
            # Abstract may have multiple sections (structured abstracts)
            abstract_texts = article.findall(".//AbstractText")
            if abstract_texts:
                parts = []
                for at in abstract_texts:
                    label = at.get("Label")
                    text = at.text or ""
                    parts.append(f"{label}: {text}" if label else text)
                abstract = " ".join(parts)
            else:
                abstract = ""
    
            rows.append({"PMID": pmid, "Title": title, "Abstract": abstract})
        return rows


    def fetch_abstracts(pmids: list[str], batch_size: int = 500) -> list[dict]:
        rows = []
        for start in tqdm.tqdm(range(0, len(pmids), batch_size)):
            batch = pmids[start: start + batch_size]
            print(f"  Fetching {start + 1}–{start + len(batch)} of {len(pmids)}...")
            try:
                with Bio.Entrez.efetch(
                    db="pubmed",
                    id=",".join(batch),
                    rettype="abstract",
                    retmode="xml",
                ) as handle:
                    xml_text = handle.read()
                rows.extend(parse_xml_abstracts(xml_text))
            except Exception as e:
                print(f"  Error on batch starting at {start}: {e}")
            time.sleep(0.11)
        return rows

    set_mouse = set(pmid for pmids in mouse['PMIDs'].apply(parse_pmids) for pmid in pmids)
    set_human = set(pmid for pmids in human['PMIDs'].apply(parse_pmids) for pmid in pmids)
    
    print(len(set_mouse), len(set_human))
    for label, pmid_set in [("mouse", set_mouse), ("human", set_human)]:
        print(f"\nFetching abstracts for {len(pmid_set)} {label} PMIDs...")
        rows = fetch_abstracts(list(pmid_set))
        df = pd.DataFrame(rows)
        out_path = f"../Allen/{label}_abstracts.csv"
        df.to_csv(out_path, index=False)
        print(f"Saved {len(df)} abstracts to {out_path}")

if __name__ == "__main__":
    main()
    



