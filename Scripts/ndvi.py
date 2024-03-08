import os
import re
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

data_path = r"D:\University\AmericaView_HLS\WW006_20230706_20230716"

tif_files = glob(os.path.join(data_path, "*.tif"))
tif_files.sort()

files_by_date = {}

for tif_file in tif_files:
    date_part = tif_file.split(".")[3]
    files_by_date.setdefault(date_part, []).append(tif_file)

# for key in files_by_date.keys():
#     print(key)

for date, files in files_by_date.items():
    arr_st, meta = es.stack(files, nodata=-9999)
    ndvi = es.normalized_diff(arr_st[4], arr_st[3])
#     output_filename = os.path.join(data_path, f"{date}_NDVI.png")
    title = f"HLS NDVI for {os.path.basename(data_path)} - Date {date}"
    ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, title=title, vmin=-1, vmax=1)
#     print(f"Successfully saved calculation for {date} as {date}_NDVI.png.")

print("All capture dates processed.")