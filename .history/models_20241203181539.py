from typing import Optional

from pydantic import BaseModel, Field, conint, constr


class Book(BaseModel):
    """Pydantic model to represent a Book with validation."""
    title: str = Field(..., min_length=1, max_length=255, title="Title of the book")
    author: str = Field(..., min_length=1, max_length=255, title="Author of the book")
    genre: str = Field(..., min_length=3, max_length=100, title="Genre of the book")
    year_published: conint(ge=1450, le=2024)  # Ensuring the year is realistic
    isbn: constr(regex=r'^(97(8|9))?\d{9}(\d|X)$')  # Validating ISBN format (ISBN-10 or ISBN-13)

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    """Pydantic model for updating book details with optional fields."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, title="Title of the book")
    author: Optional[str] = Field(None, min_length=1, max_length=255, title="Author of the book")
    genre: Optional[str] = Field(None, min_length=3, max_length=100, title="Genre of the book")
    year_published: Optional[conint(ge=1450, le=2024)] = None
    isbn: Optional[constr(regex=r'^(97(8|9))?\d{9}(\d|X)$')] = None

    class Config:
        orm_mode = True
