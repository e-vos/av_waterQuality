''' 
Filename: count_consec.py
Author: Elliot Vosburgh
Date: 7 June 2024
Description:
    Calculate the longest consecutive time that a pixel was above an NDVI threshold
'''

import arcpy

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"
table = "all_years_HLS_PointGrid_thresholdCount"

# Creating field (and check if I've had to run this a few times... ESSENTIAL FUNCTIONALITY ha)
consec_count = "Consecutive_count"
if consec_count not in [field.name for field in arcpy.ListFields(table)]:
    arcpy.AddField_management(table, consec_count, 'SHORT')

fields = [field.name for field in arcpy.ListFields(table) if field.name.startswith('Captured_')] # Some non-relevant columns are intermixed like X,Y coordinates, WW name, etc.

# Double check to make sure there are columns that start with "Captured_"...
if fields:
    with arcpy.da.UpdateCursor(table, ['OID@', consec_count] + fields) as cursor:
        for row in cursor:
            threshold_values = row[2:] # Essentially have made a virtual table, where OID and consec_count are in positions 0 and 1
            max_consec_count = 0
            count = 0
            for value in threshold_values:
                if value == 1:
                    count += 1
                    max_consec_count = max(max_consec_count, count) # Compare current count with maximum count, grab larger of the two
                else:
                    count = 0
            
            row[1] = max_consec_count # consec_count is in position 1 of the virtual table
            cursor.updateRow(row)
    print("Consecutive counts updated successfully.")
else:
    print("No capture columns found!! Error!!") # Don't let it happen again