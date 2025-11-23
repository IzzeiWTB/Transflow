import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_mongo_collection():
    mongo_url = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    mongo_db = os.getenv("MONGO_DB", "transflow_db")
    mongo_collection = os.getenv("MONGO_COLLECTION", "corridas")
    client = MongoClient(mongo_url)
    db = client[mongo_db]
    return db[mongo_collection]
