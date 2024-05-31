import pandas as pd


# filter data based on column
def filter_data(self, col, value):
    return self.df[self.df[col] == value]

