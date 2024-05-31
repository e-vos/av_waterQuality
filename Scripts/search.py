''' 
Filename: search.py
Author: Elliot Vosburgh
Date: 17 May 2024
Description:
    Query two CSV files to extract dates and NDVI values for a target waterbody.
'''

import pandas as pd
from datetime import datetime

###########################
# Definitions for the query
###########################

data_file = r'C:\Users\Elliot\Downloads\test_out.csv'

target_ww = 'Worden Pond' # Case sensitive. If you're looking for Indian Lake, do not type "indian lake" or "Indian lake"

startTime = datetime.now() # Just for timing execution time

#####################
# Advisory extraction
#####################

alert_df = pd.read_csv(r'C:\Users\Elliot\Documents\University\Internships\AV\av_waterQuality\Datasets\CSV\Filtered_Alert_WW_Stations.csv')

target_alerts = alert_df[alert_df['Waterbody'] == target_ww] # Only extract data for target_ww

advisory_dates = pd.to_datetime(target_alerts['Advisory Posted']).unique() # Extract alert dates for target_ww

print(f"Found {len(advisory_dates)} advisory dates for {target_ww}\n")

############
# Query loop
############

for adv_date in advisory_dates:
    # Define start and end dates for the query based on the advisory date
    start_date = adv_date - pd.Timedelta(days=14)
    end_date = adv_date + pd.Timedelta(days=14)

    print(f"Query begun for dates between {str(start_date)[:10]} and {str(end_date)[:10]}...")

    # Query
    df = pd.read_csv(data_file)

    datetime_format = 'Captured_%Y_%m_%d_%H%M%S' # Format from original table, ArcPro-friendly format

    filtered_data = []
    for index, row in df.iterrows():
        if row['NAME'] == target_ww:
            for column in df.columns[1:]:
                capture_date = pd.to_datetime(column, format=datetime_format)
                if start_date <= capture_date <= end_date:
                    filtered_data.append((row['NAME'], capture_date, row[column]))

    # Create DataFrame from filtered data
    filtered_df = pd.DataFrame(filtered_data, columns=['Name', 'Capture date', 'NDVI'])

    if filtered_df.empty:
        print(f"!! No data available between {str(start_date)[:10]} and {str(end_date)[:10]}. !!\n")
    else:
        print(f"{filtered_df}\n")
        
print(f"Query completed in {(datetime.now() - startTime).total_seconds():.2f} seconds.")