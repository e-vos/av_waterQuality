''' 
Filename: ndvi.py
Author: Elliot Vosburgh
Date: 13 April 2024
Description:
    Quick script to replace periods in a filename with underscores. ArcPro doesn't play nicely with '.' in filenames.
    IMPORTANT: MAKE SURE TO RUN THIS SCRIPT ON ALL FILES YOU INTEND TO USE WITH ARCPY!! AN ERROR LIKE THIS WILL
               BE THROWN OTHERWISE:
               
                ERROR 000354: The name contains invalid characters
'''

import os

def rename(directory):
    files = os.listdir(directory)
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            filename, extension = os.path.splitext(file)
            new_name = filename.replace('.', '_') + extension
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {file} to {new_name} in {directory}.")

directory_path = r"D:\University\AmericaView_HLS\2019_HLS_data\ndvi"

rename(directory_path)
