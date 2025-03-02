from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from app.models.item import Item, ItemCreate
from app.database.mongodb import get_database

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


def serialize_item(item):
    """Convert MongoDB document to Item model"""
    return {
        "_id": str(item["_id"]),
        "text": item["text"],
        "id": item.get("id"),
        "created_at": item["created_at"],
        "updated_at": item.get("updated_at")
    }


@router.get("/", response_model=List[Item])
async def read_items():
    """Get all items"""
    db = get_database()
    items = db.items.find().sort("created_at", -1)  # Sort by created_at descending
    return [serialize_item(item) for item in items]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item"""
    db = get_database()
    
    new_item = {
        "text": item.text,
        "created_at": datetime.utcnow(),
    }
    
    # Add the id field if provided in the request
    if item.id:
        new_item["id"] = item.id
    
    result = db.items.insert_one(new_item)
    
    # Get the created item
    created_item = db.items.find_one({"_id": result.inserted_id})
    
    return serialize_item(created_item)


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str):
    """Get a specific item by ID"""
    db = get_database()
    
    # First try to find the item by custom id field
    item = db.items.find_one({"id": item_id})
    
    # If not found by custom id, try to find by ObjectId
    if item is None:
        try:
            item = db.items.find_one({"_id": ObjectId(item_id)})
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid item ID format")
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return serialize_item(item) 