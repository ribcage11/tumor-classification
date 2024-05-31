import pandas as pd


class DataFrameProcessor:
    def __init__(self, df):
        self.df = df


# filter data based on column
def filter_data(self, col, value):
    result = self.df[self.df[col] == value]
    return result
