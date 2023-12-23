from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fast-mongo"]
collection = db["books"]


class Item(BaseModel):
    name: str
    description: str = None


@app.post("/items/")
async def create_item(item: Item):
    # Insert item into MongoDB
    result = collection.insert_one(item.model_dump())
    return {"id": str(result.inserted_id), **item.model_dump()}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # Retrieve item from MongoDB by ID
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    # Retrieve items from MongoDB with pagination
    items = collection.find().skip(skip).limit(limit)
    return list(items)
