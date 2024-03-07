import requests
import os

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

username = ""
password= ""
session = SessionWithHeaderRedirection(username, password)

url_string = """

"""

url_lines = url_string.strip().splitlines()
urls = url_lines

storage_path = r"D:\University\AmericaView_HLS\WW150_20231007_20231017"

with requests.Session() as session:
    for url in urls:
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