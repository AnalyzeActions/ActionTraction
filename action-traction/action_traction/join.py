"""A program to join programs as specified."""

import pandas as pd

def join(first_dataframe, second_dataframe):
    joined_dataframe = pd.DataFrame()
    joined_datafame = pd.merge(first_dataframe, second_dataframe, on="hash", how="inner")

    print(first_dataframe["hash"])
    return joined_dataframe


def perform_joining(directory_path):
    joined_dataframe = pd.DataFrame()
    first_dataframe = pd.read_csv(directory_path + "/minedRepos.csv")
    second_dataframe = pd.read_csv(directory_path + "/joke2k-faker-Workflows.csv")

    joined_dataframe = join(first_dataframe, second_dataframe)

    join_path = directory_path + "/joined.csv"

    joined_dataframe.to_csv(join_path)


