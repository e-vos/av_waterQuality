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
import csv

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
    
    # print(matches_set)
    
    '''
    
    In the case of the RIDEM alerts and WW test sites, the following waterbodies
    have one or more overlaps:
    
    ['Almy Pond', 'Barber Pond', 'Barney Pond', 'Blackamore Pond', 'Boone Lake', 'Brickyard Pond', 'Carbuncle Pond', 'Georgiaville Pond', 'Indian Lake', 'Larkin Pond', 'Mashapaug Pond', 'Scott Pond', 'Spectacle Pond', 'Stafford Pond', 'Tarkiln Pond', 'Tiogue Lake', 'Warwick Pond', 'Wenscott Reservoir', 'Worden Pond']
    
    '''

else:

    print("An error has occurred: the number of files selected does not equal " + num_files)
    
# Create SQL expression from matches_set to make a selection in ArcGIS Pro

sql_selection = "NAME IN ({})".format(', '.join(["'{}'".format(i) for i in matches_set]))

# print(sql_selection)

'''

Output:

NAME IN ('Almy Pond', 'Barber Pond', 'Barney Pond', 'Blackamore Pond', 'Boone Lake', 'Brickyard Pond', 'Carbuncle Pond', 'Georgiaville Pond', 'Indian Lake', 'Larkin Pond', 'Mashapaug Pond', 'Scott Pond', 'Spectacle Pond', 'Stafford Pond', 'Tarkiln Pond', 'Tiogue Lake', 'Warwick Pond', 'Wenscott Reservoir', 'Worden Pond')

MISSING FROM RIGIS PONDS AND LAKES SHAPEFILE: 'Boone Lake', 'Tarkiln Pond'

Explaination: Someone incorrectly spelled "Boone Lake" as "Boon Lake" and "Tarkiln Pond" as "Tarklin Pond".
              I have updated the shapefile to correct these errors. The names of waterbodies in the shapefile
              agree with the names in matches_set and sql_selection.
'''

# print(len(matches_set))

# Associate waterbody name with watershed watch station designation (WWXXX format)

names_dict = {}

filtered_df = df2[df2['Site_DESCR'].isin(matches_set)]

names_dict = dict(zip(filtered_df['WW_Station'], filtered_df['Site_DESCR']))

# print(names_dict)

'''

Output:

{'WW002': 'Barber Pond', 'WW005': 'Blackamore Pond', 'WW006': 'Boone Lake', 
'WW007': 'Brickyard Pond', 'WW016': 'Georgiaville Pond', 'WW018': 'Indian Lake', 
'WW025': 'Mashapaug Pond', 'WW049': 'Spectacle Pond', 'WW055': 'Tiogue Lake', 
'WW059': 'Warwick Pond', 'WW062': 'Wenscott Reservoir', 'WW066': 'Worden Pond', 
'WW134': 'Barney Pond', 'WW138': 'Larkin Pond', 'WW143': 'Scott Pond', 'WW145': 'Stafford Pond', 
'WW150': 'Carbuncle Pond', 'WW199': 'Almy Pond', 'WW204': 'Tarkiln Pond'}

'''

dict_df = pd.DataFrame.from_dict(names_dict, orient="index")
dict_df.to_csv(r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv")