from fastapi import FastAPI
from preset import preset
from db import get_top_k, get_favourites
import uvicorn


app = FastAPI()

@app.get("/get_top_k/{k}")
def get_tops(k: int):
    return get_top_k(k)

@app.get("/get_favourites")
def get_favs():
    return get_favourites()


if __name__ == "__main__":
    preset(days=50, refresh=False)
    uvicorn.run(app, host="0.0.0.0", port=8000)