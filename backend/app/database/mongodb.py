import os
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "debot")

# Global variables for MongoDB connection
mongo_client: Optional[MongoClient] = None
mongo_db: Optional[Database] = None

async def connect_to_mongo():
    """Connect to MongoDB when app starts"""
    global mongo_client, mongo_db
    
    try:
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client[MONGO_DB]
        
        # Ping the database to check the connection
        mongo_client.admin.command('ping')
        print(f"Connected to MongoDB at {MONGO_URI}, using database {MONGO_DB}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection when app shuts down"""
    global mongo_client
    
    if mongo_client:
        mongo_client.close()
        print("MongoDB connection closed")

def get_database() -> Database:
    """Get MongoDB database instance"""
    if mongo_db is None:
        raise Exception("MongoDB connection not established")
    return mongo_db 