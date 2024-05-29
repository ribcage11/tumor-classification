import glob
import os
import re


# Read simple config file to dictionary
def read_config(config_path='config'):
    config = {}
    with open(config_path) as file:
        for line in file:
            line = line.strip()
            key, data = line.split(':')

            key = key.strip()

            # store dictionary value as list if multiple entries with comma 
            data = data.split(',')
            # strip whitespace in all entries
            if len(data) == 1:
                data = data[0].strip()
            else:
                data = [item.strip() for item in data]

            config[key] = data
    return config


# Traverse through <patient dir> to get paths of scans sorted by their image number.
# params: <location of data/>, <data subfolder (ex. raw or processed)>, <patient ID>, <list of sequences>
def _get_sample(im_root, folder, brats21id, seq):
    im_path_arr = []  # All file paths in all sequences from the patient 
    if type(seq) is str:
        seq = [seq]

    for s in seq:
        # Gist: Match /data/<train or test>/ID/sequence/* 
        seq_paths = glob.glob(os.path.join(im_root, folder, brats21id, s, '*'))
        # get basename, then extract digits from regex, sort by int instead of alphabetical
        seq_paths = sorted(seq_paths,
                           key=lambda x: int(re.search(r'\d+', x.split('/')[-1]).group()))
        im_path_arr.extend(seq_paths)  # Flatten to list of paths 
    return im_path_arr


# Get patient IDs from label list, then _get_samples for all patients
# params: <location of data/>, <data subfolder (ex. raw or processed)>, <patient ID>, <list of sequences>
# returns: list of all patient scans (paths) in data/subfolder
def get_all_paths(im_root, folder, brats21ids, seq):
    paths = []  # nested array structured as {patient: image(2D array)}
    for b_id in brats21ids:
        # For each patient, store absolute paths of their images, UUID in flattened arrays
        sliced_path = _get_sample(im_root, folder, b_id, seq)
        paths.extend(sliced_path)
    return paths