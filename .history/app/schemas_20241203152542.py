# schemas.py

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# Define the Pydantic model for Book (Base schema)
class BookBase(BaseModel):
    title: str = Field(..., example="The Great Gatsby")
    author: str = Field(..., example="F. Scott Fitzgerald")
    published_date: Optional[date] = Field(None, example="1925-04-10")
    genre: Optional[str] = Field(None, example="Fiction")

# Schema for creating a new book (extends BookBase)
class BookCreate(BookBase):
    pass

# Schema for reading book details (includes the id for response)
class Book(BookBase):
    id: int

    class Config:
        orm_mode = True  # Ensures compatibility with SQLAlchemy models
