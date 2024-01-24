from db import *
from data_processing import *
import datetime


def last_k_days(k):
    dates = []
    today = datetime.datetime.now()
    i = 0
    count = 0
    while count < k:
        prev_i_day = today - datetime.timedelta(days=i)
        day = prev_i_day.strftime("%A")
        if day != "Saturday" and day != "Sunday":
            ddmmyy = prev_i_day.strftime("%d%m%y")
            dates.append(ddmmyy)
            count += 1
        i += 1
    
    return dates

def load_k_days(k):
    dates = last_k_days(k)
    
    for ddmmyy in dates:
        formatted_date = format_date(ddmmyy)
        
        if not data_exists(ddmmyy):
            download_by_date(ddmmyy)
            print(f"Downloaded [Day: {formatted_date}]")
        
        if data_exists(ddmmyy) and not data_exists_db(ddmmyy): 
            store_data(ddmmyy)
            print(f"Stored [Day: {formatted_date}]")
    
    close_mongo()

load_k_days(50)