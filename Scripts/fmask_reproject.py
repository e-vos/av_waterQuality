''' 
Filename: ndvi.py
Author: Elliot Vosburgh
Date: 17 April 2024
Description:
    Quick script to reproject Fmask files of HLS data split over multiple tiles.
'''

import os
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
from rasterio.crs import CRS

directory = r"D:\University\AmericaView_HLS\2019_HLS_data"

print(f"Working from {directory}...")

files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('Fmask.tif')]

common_transform = None
reprojected_files = []

for file in files:
    print(f"Reading {file}...")
    with rasterio.open(file) as src:
        dst_crs = CRS.from_epsg(32618)
        
        arr, transform = reproject(
            source=rasterio.band(src, 1),
            destination=np.zeros_like(src.read(1)),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=common_transform if common_transform else src.transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest)
        
        if common_transform is None:
            common_transform = transform
            
        reprojected_file = os.path.join(directory, f"{os.path.basename(file)}_reprojected.tif")
        
        profile = src.profile
        profile.update({
            'crs': dst_crs,
            'transform': common_transform
        })

        with rasterio.open(reprojected_file, 'w', **profile) as dst:
            dst.write(arr, 1)
        
        reprojected_files.append(reprojected_file)

print("All Fmask files reprojected successfully. Exiting...")