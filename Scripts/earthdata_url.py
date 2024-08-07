''' 
Filename: earthdata_url.py
Author: Elliot Vosburgh
Date: 5 March 2024
Description:
    Find HLS data quickly by bypassing clunky website search.
'''

# Set variables

i_date = '2019-07-09'
f_date = '2019-07-09'
cloud_cover_max = 15

# URLs

landsat_url = (
    "https://search.earthdata.nasa.gov/search/granules?p=C2021957657-LPCLOUD&"
    f"pg[0][v]=f&pg[0][qt]={i_date}%2C{f_date}&pg[0][cc][max]={cloud_cover_max}&"
    "pg[0][gsk]=-start_date&q=hls&sp[0]=-71.52539%2C41.66843&tl=1709691525!3!!&"
    "base=landWaterMap&lat=41.81784160090278&long=-71.81982421875"
)

sentinel2_url = (
    "https://search.earthdata.nasa.gov/search/granules?p=C2021957295-LPCLOUD&"
    f"pg[0][v]=f&pg[0][qt]={i_date}T00%3A00%3A00.000Z%2C{f_date}T23%3A59%3A59.999Z&"
    f"pg[0][cc][max]={cloud_cover_max}&pg[0][gsk]=-start_date&q=hls&"
    "sp[0]=-71.52979%2C41.66813&tl=1709692070.051!3!!&lat=40.93494071937711&"
    "long=-71.9560546875"
)


print(f"Landsat URL: {landsat_url}")
print(f"Sentinel-2 URL: {sentinel2_url}")