import arcpy
import datetime

arcpy.env.workspace = r"C:\Users\Elliot\Documents\University\Internships\AV\Project\AmericaView Project.gdb"

my_table = ""

fields = arcpy.ListFields(my_table)

for field in fields:
    if field.name.endswith("_NDVI"):

        original_name = field.name
        year = int(original_name[1:5])
        day_of_year = int(original_name[5:8])
        time_of_day = original_name[9:15]

        date = datetime.datetime(year, 1, 1) + datetime.timedelta(day_of_year - 1)
        formatted_date = date.strftime("%Y_%m_%d")
        
        new_column_name = f"{formatted_date}_{time_of_day}"
        
        arcpy.AlterField_management(my_table, original_name, new_column_name)