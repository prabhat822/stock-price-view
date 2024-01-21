import requests
import shutil


def date_to_url(ddmmyy):
    return f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{ddmmyy}_CSV.ZIP'

def download_by_date(ddmmyy):
    url = date_to_url(ddmmyy)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    try:
        with open(f"files/zips/EQ{ddmmyy}.zip", 'wb') as file:
            file.write(response.content)
    except:
        print("Download Error")
    
    try:
        shutil.unpack_archive(f"files/zips/EQ{ddmmyy}.zip", f"files/csvs/")
    except:
        print("Unzip Failed")

download_by_date("130124")