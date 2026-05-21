""" This script retrieves the allen brain atlas terms """
import requests
import pandas as pd
import os
def ret_words(url:str) -> list[str]:
    """ 
    This fxn retrieves a list of allen brain atlas words for mice.

    :param url: The url to retrieve the structure/words.
    :type url: str
    :returns list[str]

    """

    msg = requests.get(url).json().get('msg')

    brain_regions = []

    # DFS through the response tree and store the name of the region.
    def dfs(node):
        brain_regions.append(node.get("name"))
        for child in node.get("children", []):
            dfs(child)

    dfs(msg[0])
    return brain_regions

def store_words() -> None:
    """ 
    Stores the words in a csv file.
    
    :returns None
    """

    # Instantiate the dataframes.
    df_mouse = pd.DataFrame()
    df_human = pd.DataFrame()

    # Retrieve the words.
    df_mouse['Region'] = ret_words(url = "http://api.brain-map.org/api/v2/structure_graph_download/1.json")
    df_human['Region'] = ret_words(url ="http://api.brain-map.org/api/v2/structure_graph_download/10.json")

    # Store them into csv files in ../Allen/.
    df_mouse.to_csv("../Allen/mouse.csv")
    df_human.to_csv("../Allen/human.csv")

    return

def main():

    # Create and retrieve the words.
    # Anna was here!
    store_words()
    print("Retrieved words and stored in ../Allen/*!")

if __name__ == "__main__":
    main()
