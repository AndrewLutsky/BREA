""" This script retrieves the relevant pubmed data given a list of words. """
from brea.entrez import retrieve_pmids
import pandas as pd
import json
import Bio.Entrez 

def main():
    # Read in the csv files.
    mouse = pd.read_csv("../Allen/mouse.csv")
    human = pd.read_csv("../Allen/human.csv")
    
    with open("config.json", 'r') as f:
        config = json.load(f)
        Bio.Entrez.email = config['ENTREZ_EMAIL']
        f.close()

    mouse_regions =mouse['Region']
    mouse['PMIDs'] = [retrieve_pmids(x, api_key = config['ENTREZ_API'], additional_operators = ["Mouse"]) for x in mouse_regions]
    mouse.to_csv("../Allen/mouse.csv", index=False)

    human_regions =human['Region']
    human['PMIDs'] = [retrieve_pmids(x, api_key = config['ENTREZ_API'], additional_operators = ["Human"]) for x in human_regions]
    human.to_csv("../Allen/human.csv", index=False)



if __name__ == "__main__":
    main()
