import pandas as pd
import os
import pickle
import numpy as np
from helpers import dump_batch
from tqdm import tqdm
from gensim.models import KeyedVectors



def load_csvs(filepaths):
    """loads csv files as pandas Dataframe"""
    loaded_csvs = []
    for filepath in filepaths:
        loaded_csv = pd.read_csv(filepath)
        loaded_csvs.append(loaded_csv)
    return loaded_csvs


all_stances = ["agree", "disagree", "discuss", "unrelated"]
RELATED = all_stances[:3]

def one_hot(label, all_labels):
    """One hot encodes a label given all labels"""
    one_hot_arr = [0 for _ in range(len(all_labels))]
    for i, label_i in enumerate(all_labels):
        if label == label_i:
            one_hot_arr[i] = 1
    return one_hot_arr


def process_paths(bodies_path, stances_path):
    df_bodies, df_stances = load_csvs([bodies_path, stances_path])

    print("Stances distribution :")

    print(df_stances.groupby("Stance").size())
    headlines, bodies, one_hot_stances, stances = preprocess(
        df_stances, df_bodies)

    return headlines, bodies, one_hot_stances



def vectorize(document,max_len):
    tokens = document.split()
    tokens = tokens[:max_len]
    

def preprocess(df_stances, df_bodies):
    """Processed both dfs and returns lists of bodies, headlines, and one-hot encoded labels"""
    bodies = []
    headlines = []
    stances = []
    one_hot_stances = []
    df_body_indexed = df_bodies.set_index("Body ID")
    for headline, bodyId, stance in tqdm(df_stances.values):
        if stance.lower() in RELATED: 
            headlines.append(headline)
            body = df_body_indexed.loc[bodyId].articleBody
            bodies.append(body)
            stances.append(stance)
            one_hot_stance = one_hot(stance, all_stances)
            one_hot_stances.append(one_hot_stance)
    return headlines, bodies, one_hot_stances, stances


if __name__ == "__main__":

    all_processed = [
        process_paths("fnc-1/train_bodies.csv", "fnc-1/train_stances.csv"),
        process_paths("fnc-1/competition_test_bodies.csv","fnc-1/competition_test_stances.csv")
    ]
    headlines_all = []
    bodies_all = []
    one_hot_stances_all = []
    for (headlines,bodies,one_hot_stances) in all_processed:
      headlines_all.extend(headlines)
      bodies_all.extend(bodies)
      one_hot_stances_all.extend(one_hot_stances)

    output_folder = "related_data"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        print(f"Creating folder {output_folder}")

    dump_batch(["headlines", "bodies", "one_hot_stances"], objects=[
               headlines_all, bodies_all, one_hot_stances_all], folder_prefix=output_folder)
