''' 
Filename: rename_columns.py
Author: Elliot Vosburgh
Date: 19 April 2024
Description:
    Rename columns to something easier to read.
'''

import arcpy
import datetime

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"

my_table = "HLS_PointGrid_WW_Waterbodies_COPY" # If you're modifying another table, properties -> copy name

fields = arcpy.ListFields(my_table)

print(f"Modifying table: {my_table} within {arcpy.env.workspace}. Beginning renaming process...")

for field in fields:
    if field.name.startswith("NDVI_"):

        original_name = field.name
        year = int(original_name[5:9])
        day_of_year = int(original_name[9:12])
        time_of_day = original_name[12:].replace("T", "") # HLS filenames have the time written as "THHMMSS"

        date = datetime.datetime(year, 1, 1) + datetime.timedelta(day_of_year - 1)
        formatted_date = date.strftime("%Y_%m_%d")	# Leaving the capture time in because there are some instances of multi dates
        
        new_column_name = f"Captured_{formatted_date}_{time_of_day}"	# Col name can't start with a number...
        
        arcpy.AlterField_management(my_table, original_name, new_column_name)

print(f"All columns renamed successfully for {my_table}. Exiting...")