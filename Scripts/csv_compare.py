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

samples_yearly = {}     # Primary dictionary used to house yearly nested dictionaries

# Iterate again, like before

for filename in os.listdir(datasets_dir):

    if "_filtered" in filename and filename.endswith(".csv"):
    
        path = os.path.join(datasets_dir, filename)
        
        df_samples = pd.read_csv(path, encoding='latin1')       # "" encoding problem with UTF-8, happens with 2021 dataset
        
        year = filename.split('-')[1].split('.')[0]             # Grab year from filename (WW-YYYY.csv format)
        
        if year not in samples_yearly:                          # New nested dictionary for each year
            
            samples_yearly[year] = {}
            
        for index, row in df_samples.iterrows():
            
            station_id = row[0]
            sampling_date = row[1]
            
            samples_yearly[year][sampling_date] = station_id    # Access via print(samples_yearly['YYYY_filtered'])
                                                                # Dictionaries are useful in this use case because
                                                                # they do not allow duplicates. There are multiple
                                                                # samples per Station ID per sample date, but filing
                                                                # them in a dictionary constrains our data to only one
                                                                # sample.

# print(*samples_yearly)
# Output: 2011_filtered 2012_filtered 2013_filtered 2014_filtered 2015_filtered 2016_filtered 2017_filtered 2018_filtered 2019_filtered 2020_filtered 2021_filtered

df_alerts = pd.read_csv(r"C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv")
alerts_dict = {}

for index, row in df_alerts.iterrows():
    
    alerts_dict[row['Advisory Posted']] = row['Station_name']
    
# print(alerts_dict)

'''
Output:

{'11/20/2023': 'WW018', '10/12/2023': 'WW150', '7/28/2023': 'WW049', '7/14/2023': 'WW016', '7/11/2023': 'WW006', '10/14/2022': 'WW016', 
'9/2/2022': 'WW005', '8/5/2022': 'WW062', '7/22/2022': 'WW025', '6/27/2022': 'WW055', '6/10/2022': 'WW199', '10/7/2021': 'WW059', '9/30/2021': 'WW066', 
'9/3/2021': 'WW007', '8/6/2021': 'WW062', '7/23/2021': 'WW059', '7/13/2021': 'WW049', '6/28/2021': 'WW016', '10/19/2020': 'WW062', '9/28/2020': 'WW025', 
'9/10/2020': 'WW049', '9/4/2020': 'WW005', '8/21/2020': 'WW134', '7/16/2020': 'WW145', '7/8/2020': 'WW016', '6/24/2020': 'WW199', '8/16/2019': 'WW150', 
'8/9/2019': 'WW025', '7/10/2019': 'WW016', '9/10/2018': 'WW049', '8/31/2018': 'WW204', '8/17/2018': 'WW016', '8/10/2018': 'WW005', '7/25/2018': 'WW025', 
'6/27/2018': 'WW199', '9/27/2017': 'WW145', '9/12/2017': 'WW025', '8/18/2017': 'WW059', '7/31/2017': 'WW005', '7/24/2017': 'WW049', '7/21/2017': 'WW199', 
'9/16/2016': 'WW025', '8/25/2016': 'WW059', '4/16/2016': 'WW143', '8/18/2015': 'WW059', '7/23/2015': 'WW005', '10/9/2014': 'WW005', '9/24/2014': 'WW049', 
'7/30/2013': 'WW025', '9/14/2012': 'WW143', '9/5/2012': 'WW002', '8/28/2012': 'WW199', '8/15/2012': 'WW025', '9/23/2011': 'WW049'}
'''

matches_yearly = {}

for year, year_dict in samples_yearly.items():
    
    matches = {key: value for key, value in alerts_dict.items() if key in year_dict and alerts_dict[key] == year_dict[key]}
    
    matches_yearly[year] = matches

# for key, inner_dict in matches_yearly.items():
#   
#   print(f"{key}, {inner_dict}")

'''
Output:

2011_filtered, {}
2012_filtered, {}
2013_filtered, {}
2014_filtered, {}
2015_filtered, {}
2016_filtered, {}
2017_filtered, {}
2018_filtered, {}
2019_filtered, {}
2020_filtered, {}
2021_filtered, {}
'''