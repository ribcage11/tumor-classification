import numpy as np
import pydicom
import xarray as xr

import src.df_filters as dff

from functools import wraps
from pydicom import dcmread


# Read dicom given path
def read_dicom(path):
    image = dcmread(path).pixel_array
    return image


# Assign full 3D scan to patient stored in xarray by its patient id (pid)
def to_xarray_3d(scan, pid):
    cross_sections, height, width = np.shape(scan)
    x_coord = np.arange(0, height)
    y_coord = np.arange(0, width)
    im_index = np.arange(0, cross_sections)
    scan = xr.DataArray(scan, coords=[im_index, x_coord, y_coord,], dims=['image index', 'x', 'y',], name=pid)
    return scan


# Store cross-section of 3D scan (2D image) to xarray, named <patient id>
def to_xarray_2d(image, pid):
    height, width = np.shape(image)
    x_coord = np.arange(0, height)
    y_coord = np.arange(0, width)
    image = xr.DataArray(image, coords=[x_coord, y_coord,], dims=['x', 'y',], name=pid)
    return image


# Get full 3D scan given pid, processed in chunks of 20
def read_full_3d_scan(scans_df, pid):
    patient = dff.get_patient(scans_df, pid)
    patient = patient.to_numpy()  # convert to numpy to interate through rows
    scan = xr.concat([x for x in process_images(patient)], dim='im_index')
    return scan


# Decorator to batch process given data and batch_size
# works with non-homogenous data
def batch_processor(batch_size):
    def decorator(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            # Generator to yield batches
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                # Process the batch
                yield from func(batch, *args, **kwargs)
        return wrapper
    return decorator


# Batch contains: df of scan paths and info
@batch_processor(batch_size=20)
def process_images(batch):
    processed_batch = []
    for row in batch:
        path, pid, seq, im_id = row
        image = read_dicom(path)
        image = to_xarray_2d(image, pid)
        processed_batch.append(image)
    return processed_batch
