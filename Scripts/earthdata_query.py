''' 
Filename: earthdata_query.py
Author: Elliot Vosburgh
Date: 7 March 2024
Description:
    Modified version available from EarthData documentation site.
    Designed to download multiple files from the newline separated
    file URLs that EarthData provides at the download page.
    
    Requires valid Earthdata login credentials.
'''

import requests
import os
from config import EARTHDATA_USERNAME, EARTHDATA_PASSWORD

class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return

username = EARTHDATA_USERNAME
password= EARTHDATA_PASSWORD
session = SessionWithHeaderRedirection(username, password)

url_string = """
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B12.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B02.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B11.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.Fmask.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.SAA.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B09.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B04.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B03.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B07.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B08.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B06.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B8A.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B10.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.VAA.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B05.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.VZA.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.B01.tif
https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/HLS.S30.T18TYM.2019190T153601.v2.0/HLS.S30.T18TYM.2019190T153601.v2.0.SZA.tif
"""

url_lines = url_string.strip().splitlines()
urls = url_lines
req_band_urls = [url for url in urls if url.endswith("B03.tif") or url.endswith("B05.tif") or url.endswith("B04.tif")]

storage_path = r"D:\University\AmericaView_HLS\composites_2019"

with requests.Session() as session:
    for url in req_band_urls:
        filename = os.path.basename(url)
        file_path = os.path.join(storage_path, filename)
        with open(file_path, 'wb') as file:
            r1 = session.request('get', url)
            r = session.get(r1.url, auth=(username, password))
            if r.ok:
                file.write(r.content)
                print(f"Downloaded: {filename} to {storage_path}")
            else:
                print(f"Failed to download: {filename}")