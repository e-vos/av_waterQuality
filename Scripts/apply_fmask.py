''' 
Filename: apply_fmask.py
Author: Elliot Vosburgh
Date: 3 April 2024
Description:
    Applies Fmask (function of mask) raster to respective NDVI raster, removing clouds.
'''

import arcpy
import os

workspace = r"D:\University\AmericaView_HLS\2019_summer\ndvi" # Make sure NDVI and reprojected Fmask files are in same directory

ndvi_rasters = [raster for raster in os.listdir(workspace) if "NDVI" in raster]
fmask_rasters = [raster for raster in os.listdir(workspace) if "Fmask" in raster]

for ndvi_raster in ndvi_rasters:
    date_string = ndvi_raster.split("_NDVI")[0] # Based on ndvi.py output it will be in 0 position
    matching_fmask = [fmask for fmask in fmask_rasters if date_string in fmask] # 1 fmask for every NDVI raster
    
    if matching_fmask:
        matching_fmask = matching_fmask[0]

        ndvi_path = os.path.join(workspace, ndvi_raster)
        fmask_path = os.path.join(workspace, matching_fmask)
        
        # Load corresponding NDVI and Fmask rasters as objects
        ndvi_raster_obj = arcpy.Raster(ndvi_path)
        fmask_raster_obj = arcpy.Raster(fmask_path)
        
        # Make binary raster from Fmask (values 72, 76, and >100 are clouds)
        reclassified_fmask = arcpy.sa.Reclassify(fmask_raster_obj, "Value", "64 72 0;72 1;72 76 0;76 1;76 100 0;100 255 1", "DATA")
        
        # Set clouds equal to NoData, leaving a raster with values of 0
        set_null_fmask = arcpy.sa.SetNull(reclassified_fmask, reclassified_fmask, "VALUE = 1")
        
        # Add 0 and NoData pixels to NDVI raster, effectively removing clouds
        output_raster = os.path.join(workspace, f"NDVI_{date_string}.tif")
        final_output = arcpy.sa.Plus(set_null_fmask, ndvi_raster_obj)
        final_output.save(output_raster)
        
        print(f"Processed {date_string}. Proceeding")
        
    else:
        print(f"No matching Fmask found for {ndvi_raster}")
        
print("All operations completed. Exiting...")