from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Base model for item data"""
    text: str = Field(..., min_length=1, max_length=500)


class ItemCreate(ItemBase):
    """Model for creating a new item"""
    pass


class ItemInDB(ItemBase):
    """Model for item as stored in the database"""
    _id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class Item(ItemBase):
    """Model for item returned to client"""
    _id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 