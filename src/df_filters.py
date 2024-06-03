import pandas as pd
import xarray as xr


# filter data based on column
def filter_data(df, col, value):
    result = df[df[col] == value]
    return result


# get all data given patient
def get_patient(scans_df, pid):
    patient = scans_df[scans_df['pid'] == pid]
    return patient


# get specific file path from image_id in patient
def get_image_path(scans_df, pid, im_id):
    patient = get_patient(scans_df, pid)
    image = patient[patient['image_id'] == im_id]
    return image




