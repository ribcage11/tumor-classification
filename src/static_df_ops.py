import pandas as pd

import src.file_traversal
from src.file_traversal import get_all_paths


def fill_labels_df(labels_df):
    # Pad ID to be 5 wide
    labels_df["BraTS21ID"] = labels_df["BraTS21ID"].apply(lambda x: f'{x:05}')
    labels_df.set_index("BraTS21ID", inplace=True)
    return labels_df


def fill_scan_df(labels_df, config):
    # Store scan information for easy slicing by patient and sequence
    scans_df = get_all_paths(config["data_path"], "raw", labels_df.index, config["sequences"])
    scans_df = pd.DataFrame({"file_path": scans_df})

    # Populate df with scan information: BraTS21ID, seq, and image basename
    # split path and only grab /BraTS21ID/<seq>/<image>.dcm
    scan_info = scans_df["file_path"].str.rsplit("/", expand=True, n=3).iloc[:, 1:]
    scans_df[["BraTS21ID", "seq", "image_id"]] = scan_info

    return scans_df


