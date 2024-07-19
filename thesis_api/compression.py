from PIL import Image
from io import BytesIO
import pydicom 
import os
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000Lossless


def compress_dicom_jpeg2000(dicom_path, output_path):
    ds = pydicom.dcmread(dicom_path)
    pixel_array = ds.pixel_array
    image = Image.fromarray(pixel_array)
    buffer = BytesIO()
    image.save(buffer, format='JPEG2000', quality_mode='lossless')
    compressed_data = buffer.getvalue()

    # Encapsulate the compressed data
    encapsulated_data = encapsulate([compressed_data])
    ds.PixelData = encapsulated_data
    ds.file_meta.TransferSyntaxUID = JPEG2000Lossless
    ds.is_implicit_VR = False
    ds.is_little_endian = True
    ds.save_as(output_path)

# This is the compression algorithm from the pydicom library
from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.uid import RLELossless
path = get_testdata_file("CT_small.dcm")
ds = dcmread(path)
ds.compress(RLELossless)
ds.save_as("CT_small_rle.dcm")
