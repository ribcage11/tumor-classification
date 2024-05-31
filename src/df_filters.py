import pandas as pd

# filter data based on column

def filter_data(df, col, value):
    result = df[df[col] == value]
    return result

def