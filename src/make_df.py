import pandas as pd

import src.file_traversal
from src.file_traversal import get_all_paths


def fill_labels_df(labels_df):
    # Pad ID to be 5 wide
    labels_df.rename(columns={'BraTS21ID': 'pid'}, inplace=True)  # pid = patient id
    labels_df['pid'] = labels_df['pid'].apply(lambda x: f'{x:05}')
    labels_df.set_index('pid', inplace=True)
    return labels_df


def fill_scan_df(labels_df, config):
    # Store scan information for easy slicing by patient and sequence
    scans_df = get_all_paths(config['data_path'], 'raw', labels_df.index, config['sequences'])
    scans_df = pd.DataFrame({'file_path': scans_df})

    # Populate df with scan information: pid, seq, and image basename
    # split path and only grab /pid/<seq>/<image>.dcm
    # only take digits of image id
    scan_info = scans_df['file_path'].str.rsplit('/', expand=True, n=3).iloc[:, 1:]
    scans_df[['pid', 'seq', 'image_id']] = scan_info
    scans_df['image_id'] = scans_df['image_id'].str.extract(r'(\d+)')
    scans_df['image_id'] = scans_df['image_id'].astype(dtype='int32')  # cast image index to int

    return scans_df


