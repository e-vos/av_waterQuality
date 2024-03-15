import os
import re
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

data_path = r"D:\University\AmericaView_HLS\WW006_test_dir\cropped"

tif_files = glob(os.path.join(data_path, "*.tif"))
tif_files.sort()

files_by_date = {}
avg_ndvi_dict = {}

band_pattern = re.compile(r"\.B\d{2}\.tif$")
band_raster_files = [file for file in tif_files if band_pattern.search(file)]

for tif_file in band_raster_files:
    date_part = tif_file.split(".")[3]
    files_by_date.setdefault(date_part, []).append(tif_file)

print("Organized files by timestamp. Proceeding...")

# for key in files_by_date.keys():
#     print(key)

for date, files in files_by_date.items():
    arr_st, meta = es.stack(files, nodata=256)
    ndvi = es.normalized_diff(arr_st[4], arr_st[3])
    avg_ndvi_dict[date] = np.mean(ndvi)
#     output_filename = os.path.join(data_path, f"{date}_NDVI.png")
#     title = f"HLS NDVI for {os.path.basename(data_path)} - Date {date}"
#     ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, title=title, vmin=-1, vmax=1)
    print(f"Successfully saved average NDVI value for {date} in dictionary.")

avg_keys = list(avg_ndvi_dict.keys())
avg_keys.sort()
sorted_ndvi_dict = {i: avg_ndvi_dict[i] for i in avg_keys}

print("Ordered timestamps. Proceeding...")

for date, avg_ndvi_value in sorted_ndvi_dict.items():
    print(f"{date}: {avg_ndvi_value}")

print("All capture dates processed.")