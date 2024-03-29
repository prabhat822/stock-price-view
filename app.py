from fastapi import FastAPI
from preset import preset
from db import get_top_k, get_favourites, add_favourite, remove_favourite, search_by_name, get_price_history
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from chart_server import start_chart_ui
import threading


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/search/{name}")
def search(name: str):
    return search_by_name(name)

@app.get("/get_top_k/{k}")
def get_tops(k: int):
    return get_top_k(k)

@app.get("/get_favourites")
def get_favs():
    favs = get_favourites()
    return favs

@app.post("/add_favourite/{stock_code}")
def add_fav(stock_code: int):
    add_favourite(stock_code)
    return {"message": "Added to favourites"}

@app.delete("/remove_favourite/{stock_code}")
def remove_fav(stock_code: int):
    remove_favourite(stock_code)
    return {"message": "Removed from favourites"}

@app.get("/get_price_history/{stock_code}")
def get_history(stock_code: int):
    return get_price_history(stock_code)

def run_api_server():
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

def run_chart_ui():
    start_chart_ui("localhost", 8001)

if __name__ == "__main__":
    preset(days=50, refresh=False)
    thread1 = threading.Thread(target=run_chart_ui)
    thread1.start()
    run_api_server()
    thread1.join()