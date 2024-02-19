''' 
Filename: mask_waterbodies.py
Author: Elliot Vosburgh
Date: 19 February 2024
Description:
    Apply extract by mask on rasters.
'''

import tkinter as tk
from tkinter import filedialog
import arcpy
from arcpy import env
from arcpy.sa import *

# Prompt the user twice to select CSV files

root = tk.Tk()
root.withdraw()

num_files = 1
in_raster =

for _ in range(num_files):

    in_raster = filedialog.askopenfilename(filetypes=[("Raster image files", "*.TIF, *.tif, *.JPEG, *.jpeg, *.JPG, *.jpg, *.BMP, *.bmp, *.IMG, *.img")])
    
    if not file_selection:
        print("Selection interrupted. Exiting...")
    else:
        print(f"File selected: %s" % in_raster)
        
