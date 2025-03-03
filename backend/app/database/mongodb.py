import os
import sys
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

# Add debug information about current directory
print(f"🔍 Current working directory: {os.getcwd()}")

# Load environment variables from .env.local first if it exists, fall back to .env
env_local_path = os.path.join(os.getcwd(), '.env.local')
env_path = os.path.join(os.getcwd(), '.env')

print(f"🔍 Checking for .env.local at: {env_local_path}")
print(f"🔍 Checking for .env at: {env_path}")

if os.path.exists(env_local_path):
    print(f"🔍 Loading environment from: {env_local_path}")
    load_dotenv(env_local_path)
else:
    print(f"🔍 Loading environment from: {env_path}")
    load_dotenv(env_path)

# Print all environment variables for debugging
print(f"🔍 MONGO_URI from env: {os.getenv('MONGO_URI')}")
print(f"🔍 MONGO_DB from env: {os.getenv('MONGO_DB')}")

# Determine the correct MongoDB URI based on environment
# Check if MONGO_URI is provided in .env file - this takes priority (for MongoDB Atlas)
if os.getenv("MONGO_URI"):
    MONGO_URI = os.getenv("MONGO_URI")
    print("🌩️ Using MongoDB URI from environment: MongoDB Atlas")
# Otherwise, determine based on runtime environment
elif 'uvicorn' in sys.argv[0]:
    # Running directly with Uvicorn - use localhost
    MONGO_URI = "mongodb://localhost:27017"
    print("⚠️ Development mode detected! Using localhost for MongoDB connection")
else:
    # Running in Docker/Lando - use the service name
    MONGO_URI = "mongodb://database:27017"
    print("🐳 Docker environment detected! Using container network for MongoDB connection")

MONGO_DB = os.getenv("MONGO_DB", "debot")

print(f"🔌 Configured MongoDB URI: {MONGO_URI.split('@')[0].replace('mongodb+srv://', '').replace('mongodb://', '')}{'@' + MONGO_URI.split('@')[1] if '@' in MONGO_URI else ''}")
print(f"🔌 Full MongoDB URI being used: {MONGO_URI}")

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
        print(f"✅ Connected to MongoDB at {MONGO_URI.split('@')[0].replace('mongodb+srv://', '').replace('mongodb://', '')}{'@' + MONGO_URI.split('@')[1] if '@' in MONGO_URI else ''}, using database {MONGO_DB}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
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