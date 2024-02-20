''' 
Filename: csv_compare.py
Author: Elliot Vosburgh
Date: 15 February 2024
Description:
    Compare CSV files for matching cell values.
'''

# import tkinter as tk
# from tkinter import filedialog
import os
import pandas as pd
import datetime

########################
# I. Initial comparisons
########################

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
    
    ['Almy Pond', 'Barber Pond', 'Barney Pond', 'Blackamore Pond', 'Boone Lake', 'Brickyard Pond', 'Carbuncle Pond', 
    'Georgiaville Pond', 'Indian Lake', 'Larkin Pond', 'Mashapaug Pond', 'Scott Pond', 'Spectacle Pond', 'Stafford Pond', 
    'Tarkiln Pond', 'Tiogue Lake', 'Warwick Pond', 'Wenscott Reservoir', 'Worden Pond']
    '''

# else:
#
#    print("An error has occurred: the number of files selected does not equal " + num_files)
    
# Create SQL expression from matches_set to make a selection in ArcGIS Pro

sql_selection = "NAME IN ({})".format(', '.join(["'{}'".format(i) for i in matches_set]))

# print(sql_selection)

'''
Output:

NAME IN ('Almy Pond', 'Barber Pond', 'Barney Pond', 'Blackamore Pond', 'Boone Lake', 'Brickyard Pond', 'Carbuncle Pond', 
         'Georgiaville Pond', 'Indian Lake', 'Larkin Pond', 'Mashapaug Pond', 'Scott Pond', 'Spectacle Pond', 'Stafford Pond', 
         'Tarkiln Pond', 'Tiogue Lake', 'Warwick Pond', 'Wenscott Reservoir', 'Worden Pond')

MISSING FROM RIGIS PONDS AND LAKES SHAPEFILE: 'Boone Lake', 'Tarkiln Pond'

Explanation:  Someone incorrectly spelled "Boone Lake" as "Boon Lake" and "Tarkiln Pond" as "Tarklin Pond".
              I have updated the shapefile to correct these errors. The names of waterbodies in the shapefile
              agree with the names in matches_set and sql_selection.
'''

# print(len(matches_set))

# Associate waterbody name with watershed watch station designation (WWXXX format)

names_dict = {}

filtered_df = df2[df2['Site_DESCR'].isin(matches_set)]

names_dict = dict(zip(filtered_df['Site_DESCR'], filtered_df['WW_Station']))

# print(names_dict)

'''
Output:

{'Barber Pond': 'WW002', 'Blackamore Pond': 'WW005', 'Boone Lake': 'WW006', 'Brickyard Pond': 'WW007', 
'Georgiaville Pond': 'WW016', 'Indian Lake': 'WW018', 'Mashapaug Pond': 'WW025', 'Spectacle Pond': 'WW049', 
'Tiogue Lake': 'WW055', 'Warwick Pond': 'WW059', 'Wenscott Reservoir': 'WW062', 'Worden Pond': 'WW066', 
'Barney Pond': 'WW134', 'Larkin Pond': 'WW138', 'Scott Pond': 'WW143', 'Stafford Pond': 'WW145', 
'Carbuncle Pond': 'WW150', 'Almy Pond': 'WW199', 'Tarkiln Pond': 'WW204'}
'''

dict_df = pd.DataFrame(list(names_dict.items()), columns=['Station_name', 'Waterbody_name'])

alert_df = pd.read_csv(file1)

alert_df['Station_name'] = alert_df['Waterbody'].map(names_dict)        # Populate stations column from names_dict values

alert_df = alert_df.dropna()        # Remove alerts for waterbodies that aren't tested by Watershed Watch

alert_df.to_csv(r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv", index=False)

############################################
# II. Examine alert dates with testing dates
############################################

stnames = list(names_dict.values())     # Get station names (WWXXX) in list form

datasets_dir = r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\WW_SamplingDatasets"

# Iterate through all files in datasets_dir

for filename in os.listdir(datasets_dir):

    if filename.endswith(".csv"):
    
        path = os.path.join(datasets_dir, filename)
    
        df = pd.read_csv(path, encoding='latin1')               # Encountered encoding problem with UTF-8, using ISO-8859-1 instead
    
        check_stmatches = df.iloc[:, 0].isin(stnames)           # WW varies in their column names but the index is consistent for every year
    
        df_filtered = df[check_stmatches]
    
        new_csv = os.path.splitext(csv)[0] + "_filtered.csv"    # Don't overwrite, instead make a new CSV we can search through
        new_path = os.path.join(datasets_dir, new_csv)
        df_filtered.to_csv(new_path, index=False)

# Note: dates in MM/DD/YYYY format in second column for all WW datasets
#       dates in MM/DD/YYYY format in third column for filtered dataset

df_alerts = pd.read_csv(r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv")

samples_yearly = {}     # Primary dictionary used to house yearly nested dictionaries

# Iterate again, like before

for filename in os.listdir(datasets_dir):

    if "_filtered" in filename and filename.endswith(".csv"):
    
        path = os.path.join(datasets_dir, filename)
        
        df_samples = pd.read_csv(path, encoding='latin1')       # "" encoding problem with UTF-8, happens with 2021 dataset
        
        year = filename.split('-')[1].split('.')[0]             # Grab year from filename (WW-YYYY.csv format)
        
        if year not in samples_yearly:                          # New nested dictionary for each year
            
            samples_yearly[year] = {}
            
        for index_row in df_samples.iterrows():
            
            station_id = row[0]
            sampling_date = row[1]
            
            samples_yearly[year][sampling_date] = station_id    # Access via print(samples_yearly['YYYY_filtered'])
                                                                # Dictionaries are useful in this use case because
                                                                # they do not allow duplicates. There are multiple
                                                                # samples per Station ID per sample date, but filing
                                                                # them in a dictionary constrains our data to only one
                                                                # sample.
