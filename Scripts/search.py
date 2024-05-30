''' 
Filename: search.py
Author: Elliot Vosburgh
Date: 17 May 2024
'''

import pandas as pd

# Definitions for the query
data_file = r'C:\Users\Elliot\Downloads\test_out.csv'

target_ww = 'Carbuncle Pond'

target_date = pd.to_datetime('2023-02-10') # Use the date given in "Advisory Posted"
start_date = target_date - pd.Timedelta(days=14)
end_date = target_date + pd.Timedelta(days=14)

print(f"Beginning query within {data_file} for dates between {start_date} and {end_date}...")

# Query
df = pd.read_csv(data_file)

datetime_format = 'Captured_%Y_%m_%d_%H%M%S' # This format is weird but plays nicely with ArcPro

filtered_data = []
for index, row in df.iterrows():
    if row['NAME'] == target_ww:
        for column in df.columns[1:]:
            capture_date = pd.to_datetime(column, format=datetime_format)
            if start_date <= capture_date <= end_date:
                filtered_data.append((row['NAME'], capture_date, row[column]))

# ~df from filtered data~
filtered_df = pd.DataFrame(filtered_data, columns=['Name', 'Capture date', 'NDVI'])

print(filtered_df)