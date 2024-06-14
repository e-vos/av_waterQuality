''' 
Filename: count_sum.py
Author: Elliot Vosburgh
Date: 1 June 2024
Description:
    Sum totals by year into new field.
'''

import arcpy

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"
table = "all_years_HLS_PointGrid_thresholdCount"

# Add a new field to the table (CHANGE THIS FOR EACH NEW YEAR being calc'd i.e. 2023 -> 2022 for all occurences)
arcpy.management.AddField(table, "total_2023", "LONG")

# iterate through the rows of the table
with arcpy.da.UpdateCursor(table, "*") as cursor:
    for row in cursor:
        # Initialize a variable to store the sum
        total = 0
        # Iterate through each field in the row
        for i in range(len(row)):
            # Check if the field is numeric and not OBJECTID, Shape_Length, and Shape_Area
            if isinstance(row[i], (int, float, complex)) and cursor.fields[i] not in ['OBJECTID', 'Shape_Length', 'Shape_Area'] and "2023" in cursor.fields[i]:
                # Add the field's value to the total
                total += row[i]
        # Update the new field with the total
        row[cursor.fields.index('total_2023')] = total
        cursor.updateRow(row)
