import os
import pandas as pd


def load_table(table_name, dataset):
    data_path = os.path.join("data", "{}.stackexchange.com".format(dataset))
    return pd.read_csv(os.path.join(data_path, table_name + ".csv"))


def load_scifi_table(table_name):
    return load_table(table_name, "scifi")
