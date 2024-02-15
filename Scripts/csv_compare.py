''' 
Filename: csv_compare.py
Author: Elliot Vosburgh
Date: 15 February 2024
Description:
    Compare CSV files for matching cell values.
'''

import tkinter as tk
from tkinter import filedialog
import pandas as pd

file_paths = []     # Initialize list to store selected file paths
num_files = int(2)  # Define the number of files to be read

# file1 =                       # If you have the file paths already,
# file2 =                       # use these lines to define the paths
# file_paths.append(file1)      # and comment out the prompt section
# file_paths.append(file2)      # below.

# Prompt the user twice to select CSV files

root = tk.Tk()
root.withdraw()

for _ in range(num_files):

    file_selection = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if not file_selection:
        print("No file selected. Exiting...")
    else:
        file_paths.append(file_selection)
        
# print(file_paths)

# Perform comparison and print uniques

if len(file_paths) == num_files:

    df1 = pd.read_csv(file_paths[0])
    df2 = pd.read_csv(file_paths[1])
    
    merged_df = pd.merge(df1, df2, left_on='Waterbody', right_on='Site_DESCR', how='inner')
    
    matches_verbose = merged_df['Waterbody'].tolist()
    
    matches_set = list(set(matches_verbose))    # No repeats
    
    print(matches_set)
    
    '''
    
    In the case of the RIDEM alerts and WW test sites, the following waterbodies
    have one or more overlaps:
    
    ['Barber Pond', 'Brickyard Pond', 'Spectacle Pond', 'Larkin Pond', 'Scott Pond', 'Indian Lake', 'Almy Pond', 'Blackamore Pond', 'Warwick Pond', 'Tiogue Lake', 'Stafford Pond', 'Worden Pond', 'Wenscott Reservoir', 'Boone Lake', 'Mashapaug Pond', 'Georgiaville Pond', 'Tarkiln Pond', 'Barney Pond', 'Carbuncle Pond']
    
    '''

else:

    print("An error has occurred: the number of files selected does not equal " + num_files)