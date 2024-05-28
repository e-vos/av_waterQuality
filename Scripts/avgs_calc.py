''' 
Filename: avgs_calc.py
Author: Elliot Vosburgh
Date: 13 May 2024
Description:
    Calculate average NDVI for each capture date using water body as case.
'''

import arcpy
import csv	# Output for use in Excel later
from collections import defaultdict

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"
input_table = "HLS_PointGrid_WW_Waterbodies_COPY"
output_table = r"C:\Users\Elliot\Downloads\test_out.csv"

ndvi_values = defaultdict(lambda: defaultdict(list)) # Setting up nested dictionaries...

fields = [field.name for field in arcpy.ListFields(input_table)]

# Zero positions for cols
waterbody_index = 3
date_index = 5

with arcpy.da.SearchCursor(input_table, fields) as cursor:
    
    for row in cursor:
        waterbody_name = row[waterbody_index]
        ndvi_values_row = row[date_index:]
        
        for index, ndvi_value in enumerate(ndvi_values_row):
            if ndvi_value is not None: # Could also add on a < -1 or > 1 but we already did that during NDVI calculation
                ndvi_date = fields[date_index + index]
                ndvi_values[waterbody_name][ndvi_date].append(ndvi_value)

print("Non-null values stored. Starting average calculations...")
                
average_ndvi_results = []

capture_dates = sorted(set(date for dates in ndvi_values.values() for date in dates.keys()))

for waterbody_name, dates in ndvi_values.items():
    
    average_ndvi_row = [waterbody_name]
    for date in capture_dates:
        ndvi_list = dates.get(date, [])
        if ndvi_list:
            average_ndvi = sum(ndvi_list) / len(ndvi_list)
            average_ndvi_row.append(average_ndvi)
        else:
            average_ndvi_row.append(None)
            
    average_ndvi_results.append(average_ndvi_row)

with open(output_table, 'w', newline='') as csvfile:
    
    writer = csv.writer(csvfile)
    writer.writerow(['NAME'] + capture_dates)
    writer.writerows(average_ndvi_results)
    
print("Script finished. Exiting...")