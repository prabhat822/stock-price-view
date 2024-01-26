import pandas as pd
from pymongo import MongoClient
from data_processing import is_greater_date
from datetime import datetime


def load_csv_by_date(ddmmyy):
    path = f"files/csvs/EQ{ddmmyy}.csv"
    df = pd.read_csv(path)
    
    datas = []
    for index, row in df.iterrows():
        data = {
            "code": row["SC_CODE"],
            "name": row["SC_NAME"].strip(),
            "open": row["OPEN"],
            "high": row["HIGH"],
            "low": row["LOW"],
            "close": row["CLOSE"]
        }
        datas.append(data)
    
    return datas

def store_data(ddmmyy):
    datas = load_csv_by_date(ddmmyy)
    
    collection = db[f"EQ{ddmmyy}"]
    
    collection.insert_many(datas)

    for data in datas: 
        update_metadata_one(data, ddmmyy)

def remove_data(ddmmyy):
    collection = db[f"EQ{ddmmyy}"]
    
    collection.drop()

def data_exists_db(ddmmyy):
    collection = db[f"EQ{ddmmyy}"]
    
    return collection.count_documents({}) > 0

def close_mongo():
    client.close()

def update_metadata_one(data, ddmmyy):
    CODE = data["code"]
    exists = metadata_collection.count_documents({"code": CODE}) > 0
    if not exists:
        stock = {
            "code": CODE,
            "name": data["name"],
            "latest": ddmmyy,
            "latest_close": data["close"],
            "first": ddmmyy,
            "first_close": data["close"],
            "pnl": 0,
        }
        metadata_collection.insert_one(stock)
    else:
        stock = metadata_collection.find_one({"code": CODE})
        latest = stock["latest"]
        first = stock["first"]
        if is_greater_date(ddmmyy, latest):
            pnl = ((data["close"] - stock["first_close"]) / stock["first_close"]) * 100
            metadata_collection.update_one({"code": CODE}, {"$set": {"latest": ddmmyy, "latest_close": data["close"], "pnl": pnl}})
        elif is_greater_date(first, ddmmyy):
            pnl = ((stock["latest_close"] - data["close"]) / data["close"]) * 100
            metadata_collection.update_one({"code": CODE}, {"$set": {"first": ddmmyy, "first_close": data["close"], "pnl": pnl}})

def get_top_k(k):
    top_ks = metadata_collection.find().sort("pnl", -1).limit(k)
    tks = []
    for ki in top_ks:
        tki = {
            "code": ki["code"],
            "name": ki["name"],
            "pnl": ki["pnl"]
        }
        tks.append(tki)
    
    return tks

def search_by_name(name):
    search = metadata_collection.find({"$text": {"$search": name}})
    results = []
    for result in search:
        result.pop("_id")
        results.append(result)
    
    return results

def get_by_code(code):
    stock = metadata_collection.find_one({"code": code})
    return stock

def add_favourite(stock_code):
    exists = favourites_collection.count_documents({"code": stock_code}) > 0
    if not exists:
        stock = get_by_code(stock_code)
        if stock:
            favourites_collection.insert_one(stock)

def remove_favourite(stock_code):
    exists = favourites_collection.count_documents({"code": stock_code}) > 0
    if exists:
        favourites_collection.delete_one({"code": stock_code})

def get_favourites():
    favs = []
    for f in favourites_collection.find({}):
        f.pop("_id")
        favs.append(f)
    
    return favs

def get_price_history(stock_code):
    collects = db.list_collection_names()
    days = [s[2:] for s in collects]
    days_objects = [datetime.strptime(day, "%d%m%y") for day in days]
    sorted_days_objects = sorted(days_objects)
    sorted_days = [day_obj.strftime("%d%m%y") for day_obj in sorted_days_objects]
    
    days = []
    prices = []
    for day in sorted_days:
        eq_ = db[f'EQ{day}']
        stock = eq_.find_one({"code": stock_code})
        if stock:
            days.append(day)
            prices.append(stock["close"])
    
    data = {
        "days": days,
        "prices": prices
    }
    
    return data

def clean_db():
    client.drop_database("bse")
    client.drop_database("bse_metadata")
    
    db = client["bse"]
    db_metadata = client["bse_metadata"]
    metadata_collection = db_metadata["metadata"]
    metadata_collection.create_index([('name', 'text')])
    favourites_collection = db_metadata["faviourites"]


client = MongoClient()
db = client["bse"]
db_metadata = client["bse_metadata"]
metadata_collection = db_metadata["metadata"]
metadata_collection.create_index([('name', 'text')])
favourites_collection = db_metadata["faviourites"]