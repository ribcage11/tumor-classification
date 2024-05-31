import pydicom
from pydicom import dcmread


# Read dicom given path
def read_dicom(path):
    image = dcmread(path).pixel_array
    return image
