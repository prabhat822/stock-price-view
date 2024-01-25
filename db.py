import pandas as pd
from pymongo import MongoClient
from data_processing import is_greater_date


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


client = MongoClient()
db = client["bse"]
db_metadata = client["bse_metadata"]
metadata_collection = db_metadata["metadata"]