''' 
Filename: ndvi.py
Author: Elliot Vosburgh
Date: 1 March 2024
Description:
    Calculate NDVI for input datasets and save the rasters for future analysis.
'''

# import arcpy
# from arcpy.sa import *
import os
import re
from glob import glob
import numpy as np
import rasterio
from rasterio.crs import CRS
import earthpy.spatial as es

data_path = r"D:\University\NRS516_HLS\type1_raw" # Source directory
ndvi_path = r"D:\University\NRS516_HLS\type1 _ndvi" # Output directory

# Not all files are in tif format; filtering steps
tif_files = glob(os.path.join(data_path, "*.tif"))
tif_files.sort()

files_by_date = {} # Storage for timestamps and filenames

# Just band tifs
band_pattern = re.compile(r"\.B\d{2}\.tif$")
band_raster_files = [file for file in tif_files if band_pattern.search(file)]

# Populating files_by_date
for tif_file in band_raster_files:
    date_part = tif_file.split(".")[3]
    # new_name = date_part.split("T")[0]
    files_by_date.setdefault(date_part, []).append(tif_file)

print("Organized files by timestamp. Proceeding...")

# Check the nodata value for a band
# band_path = r"D:\University\AmericaView_HLS\WW006_test_dir\HLS.L30.T18TYM.2022171T152651.v2.0.B07.tif"
# with rasterio.open(band_path) as src1:
#     nodata_value = src1.nodata
#     print("Nodata value: ", nodata_value) # For HLS, found to be -9999

# Check for incomplete bands by alerting if less than 10 exist for a given date
# for date, files in files_by_date.items():
#     if len(files) < 10:
#         print(f"ALERT: {date} dataset has only {len(files)} associated files!!")

# def applyCloudMask(input_raster, cloud_mask):
#     cloud_values = "VALUE > 100 OR VALUE = 76 OR VALUE = 72"
#     output_raster = arcpy.sa.Con(cloud_mask, -9999, input_raster, cloud_values)
#     return output_raster

for date, files in files_by_date.items():
    arr_st, meta = es.stack(files, nodata=-9999) # See above debugging test
    ndvi = es.normalized_diff(arr_st[1], arr_st[0]) # B5 = NIR, B4 = Red in HLS datasets...
    ndvi_masked = np.where((ndvi >= -1) & (ndvi <= 1), ndvi, -9999)

    output_filename = os.path.join(ndvi_path, f"{date}_NDVI.tif")
    
    # Settings for our NDVI output raster
    profile = {
        'driver': 'GTiff',
        'width': arr_st.shape[2],
        'height': arr_st.shape[1],
        'count': 1,
        'dtype': 'float32',
        'crs': CRS.from_epsg(32610),
        'transform': meta['transform'],
        'compress': 'lzw',
        'nodata': -9999
        }
    
    # Write to our output directory
    with rasterio.open(output_filename, 'w', **profile) as dst:
        dst.write(ndvi_masked, 1) # '1' is the position, it's also the only band

    print(f"Successfully saved NDVI for {date} as {output_filename}.")


print("All capture dates processed.")

# TEST FILTERING FOR OUT-OF-BOUNDS VALUES!!
# test_raster = r"D:\University\AmericaView_HLS\ndvi\2022171T152651_NDVI.tif"
# 
# with rasterio.open(test_raster) as src:
#     preproc_data = src.read(1, masked=True) # nodata = -9999, will affect stats if included
#     mask = preproc_data.mask
#     raster_data = preproc_data[~mask] # Mask out nodata
#     print(raster_data.min())
#     print(raster_data.max())