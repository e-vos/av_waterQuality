''' 
Filename: threshold_count.py
Author: Elliot Vosburgh
Date: 1 June 2024
Description:
    Count how many pixels per waterbody exceed a certain NDVI value threshold.
'''

import arcpy
import csv
from collections import defaultdict

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"
input_table = "HLS_PointGrid_WW_Waterbodies_COPY"
output_table = r"C:\Users\Elliot\Downloads\threshold_out.csv" # for Excel workflow

threshold_counts = defaultdict(lambda: defaultdict(list))

fields = [field.name for field in arcpy.ListFields(input_table)]

# Zero positions for cols
id_index = 2
waterbody_index = 3
location_index = 5
date_index = 6


with arcpy.da.SearchCursor(input_table, fields) as cursor:
    
    for row in cursor:
        pointid = row[id_index]
        waterbody_name = row[waterbody_index]
        ndvi_values_row = row[date_index:]
        
        for index, ndvi_value in enumerate(ndvi_values_row):
            if ndvi_value is not None: # Could also add on a < -1 or > 1 but we already did that during NDVI calculation
                ndvi_date = fields[date_index + index]
                if ndvi_value > 0.15:
                    if ndvi_date not in threshold_counts[pointid]:
                        threshold_counts[pointid][ndvi_date] = 1
                    else:
                        threshold_counts[pointid][ndvi_date] += 1

capture_dates = sorted(set(date for counts in threshold_counts.values() for date in counts.keys()))

with open(output_table, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['POINT'] + list(capture_dates))
    for point, counts in threshold_counts.items():
        row = [point] + [counts[date] for date in capture_dates]
        writer.writerow(row)