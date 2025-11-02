import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
# from pymongo import MongoClient

app = FastAPI()
load_dotenv()

mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_host = os.getenv("MONGO_HOST")


MONGO_URI = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_host}/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("FastAPI_GitAct")


@app.get("/")
async def tester():
    return {"collection": await db.list_collection_names()}


@app.post("/add_item/")
async def create_item(item: dict):
    result = await db.items.insert_one(item)
    return {"inserted_id": str(result.inserted_id)}


@app.get("/get_items/")
async def read_items():
    # Create a list to hold the items
    items = []

    # Cursor to iterate over the documents in the collection.
    cursor = db.items.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        items.append(document)
    return items
