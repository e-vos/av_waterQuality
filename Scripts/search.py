''' 
Filename: search.py
Author: Elliot Vosburgh
Date: 17 May 2024
Description:
    Query two CSV files to extract dates and NDVI values for a target waterbody.

    Example output:

        Found 2 advisory dates for Carbuncle Pond

        Query begun for dates between 2023-09-28 and 2023-10-26...

        Advisory period data:
                     Name        Capture date      NDVI
        0  Carbuncle Pond 2023-10-04 15:40:09  0.140165
        1  Carbuncle Pond 2023-10-05 15:27:13  0.257495
        2  Carbuncle Pond 2023-10-13 15:27:19  0.208456

        Average advisory period NDVI: 0.2020386570602207

        Preadvisory data:
                     Name        Capture date      NDVI
        0  Carbuncle Pond 2023-09-14 15:39:09  0.116849
        1  Carbuncle Pond 2023-09-21 15:35:59  0.195165
        2  Carbuncle Pond 2023-09-27 15:27:06       NaN

        Average preadvisory NDVI: 0.15600703300621643

        Query begun for dates between 2019-08-02 and 2019-08-30...

        !! No data available between 2019-08-02 and 2019-08-30. !!

        !! No data available between 2019-07-19 and 2019-08-02. !!

        Query completed in 0.03 seconds.
'''

import pandas as pd
from datetime import datetime
import numpy as np
import warnings

###########################
# Definitions for the query
###########################

data_file = r'C:\Users\Elliot\Downloads\test_out.csv'

target_ww = 'Carbuncle Pond' # Case sensitive. If you're looking for Indian Lake, do not type "indian lake" or "Indian lake"

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
    preadv_date = start_date - pd.Timedelta(days=14)

    print(f"Query begun for dates between {str(start_date)[:10]} and {str(end_date)[:10]}...\n")

    # Query
    df = pd.read_csv(data_file)

    datetime_format = 'Captured_%Y_%m_%d_%H%M%S' # Format from original table, ArcPro-friendly format

    preadv_filtered_data = []
    filtered_data = []
    for index, row in df.iterrows():
        if row['NAME'] == target_ww:
            for column in df.columns[1:]:
                capture_date = pd.to_datetime(column, format=datetime_format)
                if start_date <= capture_date <= end_date:
                    filtered_data.append((row['NAME'], capture_date, row[column]))
                if preadv_date <= capture_date <= start_date:
                    preadv_filtered_data.append((row['NAME'], capture_date, row[column]))

    # Create DataFrame from filtered data
    filtered_df = pd.DataFrame(filtered_data, columns=['Name', 'Capture date', 'NDVI'])
    preadv_df = pd.DataFrame(preadv_filtered_data, columns=['Name', 'Capture date', 'NDVI'])
    
    # Need to ignore runtime warning because preadv_ndvi_avg is sometimes NaN
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        adv_ndvi_avg = np.nanmean(filtered_df['NDVI'].tolist())
        preadv_ndvi_avg = np.nanmean(preadv_df['NDVI'].tolist())

    if filtered_df.empty:
        print(f"!! No data available between {str(start_date)[:10]} and {str(end_date)[:10]}. !!\n")
    else:
        print(f"\033[1mAdvisory period data:\033[0m\n{filtered_df}\n")
        print(f"\033[1mAverage advisory period NDVI:\033[0m {adv_ndvi_avg}\n")
        
    if preadv_df.empty:
        print(f"!! No data available between {str(preadv_date)[:10]} and {str(start_date)[:10]}. !!\n")
    else:
        print(f"\033[1mPreadvisory data:\033[0m\n{preadv_df}\n")
        print(f"\033[1mAverage preadvisory NDVI:\033[0m {preadv_ndvi_avg}\n")
        
print(f"Query completed in {(datetime.now() - startTime).total_seconds():.2f} seconds.")