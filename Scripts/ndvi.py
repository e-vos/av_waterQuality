''' 
Filename: ndvi.py
Author: Elliot Vosburgh
Date: 1 March 2024
Description:
    Calculate NDVI for input datasets and save the rasters for future analysis.
'''

import os
import re
from glob import glob
import numpy as np
import rasterio
import earthpy.spatial as es

data_path = r"D:\University\AmericaView_HLS\WW006_test_dir"
ndvi_path = r"D:\University\AmericaView_HLS\ndvi"

tif_files = glob(os.path.join(data_path, "*.tif"))
tif_files.sort()

files_by_date = {}

band_pattern = re.compile(r"\.B\d{2}\.tif$")
band_raster_files = [file for file in tif_files if band_pattern.search(file)]

for tif_file in band_raster_files:
    date_part = tif_file.split(".")[3]
    files_by_date.setdefault(date_part, []).append(tif_file)

print("Organized files by timestamp. Proceeding...")

# Check the nodata value for a band
# band_path = band_path = r"D:\University\AmericaView_HLS\WW006_test_dir\HLS.L30.T18TYM.2022171T152651.v2.0.B07.tif"
# with rasterio.open(band_path) as src1:
#     nodata_value = src1.nodata
#     print("Nodata value: ", nodata_value)

# Check for incomplete bands by alerting if less than 10 exist for a given date
# for date, files in files_by_date.items():
#     if len(files) < 10:
#         print(f"ALERT: {date} dataset has only {len(files)} associated files!!")

for date, files in files_by_date.items():
    arr_st, meta = es.stack(files, nodata=-9999)	# See above debugging test
    ndvi = es.normalized_diff(arr_st[5], arr_st[4]) # B5 = NIR, B4 = Red in HLS datasets...

    output_filename = os.path.join(ndvi_path, f"{date}_NDVI.tif")

    with rasterio.open(files[0]) as src:
        profile = src.profile
        profile.update(dtype=rasterio.float32, count=1, compress='lzw')
        profile.update({'crs': src.crs, 'transform': src.transform})
        with rasterio.open(output_filename, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)

    print(f"Successfully saved NDVI for {date} as {output_filename}.")

print("All capture dates processed.")
