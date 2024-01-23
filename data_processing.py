import requests
import shutil
import os


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
    
    try:
        os.remove(f"files/zips/EQ{ddmmyy}.zip") # Cleaning downloaded zips
    except:
        print("Deletion Error")

def data_exists(ddmmyy):
    return os.path.exists(f"files/csvs/EQ{ddmmyy}.csv")

def generate_dir():
    if not os.path.exists("files"):
        os.mkdir("files")
    if not os.path.exists("files/zips"):
        os.mkdir("files/zips")
    if not os.path.exists("files/csvs"):
        os.mkdir("files/csvs")