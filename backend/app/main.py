from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routes import items
from app.database.mongodb import close_mongo_connection, connect_to_mongo

# Load environment variables
load_dotenv()

# Get API prefix from env
API_PREFIX = os.getenv("API_PREFIX", "/api")

app = FastAPI(
    title="Debot API",
    description="API for Debot application",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://debot.deterbrown.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include routers
app.include_router(items.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Welcome to Debot API. Go to /docs for the API documentation."} 