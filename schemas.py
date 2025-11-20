"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (retain as references):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Manhwa forum specific schemas

class Post(BaseModel):
    """
    Manhwa recommendations and reviews posted by users.
    Collection name: "post"
    """
    title: str = Field(..., min_length=2, max_length=200, description="Manhwa title or post headline")
    summary: Optional[str] = Field(None, max_length=2000, description="Short description or why you recommend it")
    rating: Optional[float] = Field(None, ge=0, le=10, description="Rating out of 10")
    genres: Optional[List[str]] = Field(default_factory=list, description="List of genres or tags")
    links: Optional[List[HttpUrl]] = Field(default_factory=list, description="Related links (official, fandom, sources)")
    image_urls: Optional[List[HttpUrl]] = Field(default_factory=list, description="Image URLs to display for the post")
    image_data: Optional[List[str]] = Field(default_factory=list, description="Optional base64-encoded inline images")
    author: Optional[str] = Field(None, max_length=100, description="Display name of the author")
