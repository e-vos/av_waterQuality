''' 
Filename: access_data.py
Author: Elliot Vosburgh
Date: 15 February 2024
Description:
    Search and bulk download remote sensing data.
'''

#########
# Imports 
#########

import ee
# import numpy as np
import pandas as pd
# import geopandas as gpd
# import os, shutil
# from scipy.stats import norm, gamma, f, chi2
from datetime import datetime, timedelta
# import os

###############################################
# Initialize the project in Google Earth Engine
###############################################

ee.Authenticate()
ee.Initialize(project='av-uri-wq')

####################
# Date range testing
####################

ridem_df = pd.read_csv(r'C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv')
ridem_df['Advisory Posted'] = pd.to_datetime(ridem_df['Advisory Posted'], format='%m/%d/%Y')
advisory_dates = ridem_df['Advisory Posted']

def dateRange(advisory_date):
    i_date = advisory_date - timedelta(days=5)
    f_date = advisory_date + timedelta(days=5)
    # return i_date.strftime('%Y-%m-%d'), f_date.strftime('%Y-%m-%d')
    return i_date, f_date

# Add a +/- 5 day range to the filtered dataset using dateRange
ridem_df[['i_date', 'f_date']] = ridem_df['Advisory Posted'].apply(lambda x: pd.Series(dateRange(x)))
ridem_df.to_csv(r'C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv', index=False)

# for advisory_date in ridem_df['Advisory Posted']:
#     i_date, f_date = dateRange(advisory_date)
#     print(f"Advisory posted: {advisory_date.strftime('%Y-%m-%d')}, created range {i_date} to {f_date}")

# scan_counts = {}	# Initialize dictionary for storing date ranges/scan counts

# def countScans(i_date, f_date):
#     aoi_shp_path = r'projects/av-uri-wq/assets/RIDEM_WW_Waterbodies'
#     study_area = ee.FeatureCollection(aoi_shp_path)
#     landsat = (ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
#                .filterBounds(study_area)
#                .filterDate(ee.Date(i_date), ee.Date(f_date))
#                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 25)))
#     sentinel = (ee.ImageCollection('COPERNICUS/S2')
#                 .filterBounds(study_area)
#                 .filterDate(ee.Date(i_date), ee.Date(f_date))
#                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 25)))
#     print(f"Beginning landsat counts for date range {i_date} through {f_date}...")
#     landsat_count = landsat.size().getInfo()
#     print("Successful.")
#     print(f"Beginning sentinel counts for date range {i_date} through {f_date}")
#     sentinel_count = sentinel.size().getInfo()
#     print("Successful.")
#     return landsat_count, sentinel_count

# # Iterate through advisory dates to get counts of matching imagery for the AOI
# for advisory_date in ridem_df['Advisory Posted']:
#     i_date, f_date = dateRange(advisory_date)
#     landsat_count, sentinel_count = countScans(i_date, f_date)
#     dates_key = f"{i_date} to {f_date}"
#     scan_counts[dates_key] = {'Landsat 8': landsat_count, 'Sentinel 2': sentinel_count}

# print(scan_counts)

# # Export scan_counts to dictionary...
# scan_counts_df = pd.DataFrame.from_dict(scan_counts, orient='index')
# sc_csv_path = r'C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\scan_counts.csv'
# scan_counts_df.to_csv(sc_csv_path, index_label='Date Range')

# # Only print keys whose landsat or sentinel counts are greater than 0
# for date_range, counts in scan_counts.items():
#     landsat_count = counts['Landsat 8']
#     sentinel_count = counts['Sentinel 2']
#     if landsat_count > 0 or sentinel_count > 0:
#         print(f"Date Range: {date_range}, Landsat 8 Count: {landsat_count}, Sentinel 2 Count: {sentinel_count}")

