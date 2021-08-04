import pandas as pd

def join_datasets(path_one, path_two, key):
    data_one = pd.read_csv(str(path_one))
    data_two = pd.read_csv(str(path_two))
    merged = pd.merge(data_one, data_two, how="inner", on=[str(key)])

    merged.to_csv("/home/mkapfhammer/Documents/try_faker/final_merged_data.csv")