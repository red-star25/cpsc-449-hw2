# schemas.py

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# Define the Pydantic model for Book
class BookBase(BaseModel):
    title: str = Field(..., example="The Great Gatsby")
    author: str = Field(..., example="F. Scott Fitzgerald")
    published_date: Optional[date] = Field(None, example="1925-04-10")
    genre: Optional[str] = Field(None, example="Fiction")

# Schema for creating a new book
class BookCreate(BookBase):
    pass

# Schema for reading book details, includes the id
class Book(BookBase):
    id: int

    class Config:
        orm_mode = True