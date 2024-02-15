''' 
Filename: csv_compare.py
Author: Elliot Vosburgh
Date: 15 February 2024
Description:
    Compare CSV files for matching cell values.
'''

# import tkinter as tk
# from tkinter import filedialog
import pandas as pd

file_paths = []     # Initialize list to store selected file paths
num_files = int(2)  # Define the number of files to be read

file1 = r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\RIDEM_Cyanobacteria_Advisories_thru23.csv"
file2 = r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\WW_Test_Sites.csv"
file_paths.append(file1)
file_paths.append(file2)
col1_header = 'Waterbody'
col2_header = 'Site_DESCR'

'''
FOR FUTURE IMPLEMENTATION

# Prompt the user twice to select CSV files

root = tk.Tk()
root.withdraw()

for _ in range(num_files):

    file_selection = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if not file_selection:
        print("No file selected. Exiting...")
    else:
        col_name = input("For the selected file, what column will be used? ")
        
        file_paths.append(file_selection, col_name)
        
# print(file_paths)
'''

# Perform comparison and print uniques

if len(file_paths) == num_files:

    df1 = pd.read_csv(file_paths[0])
    df2 = pd.read_csv(file_paths[1])
    
    merged_df = pd.merge(df1, df2, left_on=col1_header, right_on=col2_header, how='inner')
    
    matches_verbose = merged_df[col1_header].tolist()
    
    matches_set = sorted(list(set(matches_verbose)))    # No repeats
    
    print(matches_set)
    
    '''
    
    In the case of the RIDEM alerts and WW test sites, the following waterbodies
    have one or more overlaps:
    
    ['Almy Pond', 'Barber Pond', 'Barney Pond', 'Blackamore Pond', 'Boone Lake', 'Brickyard Pond', 'Carbuncle Pond', 'Georgiaville Pond', 'Indian Lake', 'Larkin Pond', 'Mashapaug Pond', 'Scott Pond', 'Spectacle Pond', 'Stafford Pond', 'Tarkiln Pond', 'Tiogue Lake', 'Warwick Pond', 'Wenscott Reservoir', 'Worden Pond']
    
    '''

else:

    print("An error has occurred: the number of files selected does not equal " + num_files)