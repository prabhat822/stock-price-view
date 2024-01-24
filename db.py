import pandas as pd
from pymongo import MongoClient


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

def remove_data(ddmmyy):
    collection = db[f"EQ{ddmmyy}"]
    
    collection.drop()

def data_exists_db(ddmmyy):
    collection = db[f"EQ{ddmmyy}"]
    
    return collection.count_documents({}) > 0

def close_mongo():
    client.close()


client = MongoClient()
db = client["bse"]
