from typing import Optional

from pydantic import BaseModel, Field, validator


class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, example="The Great Gatsby")
    author: str = Field(..., min_length=1, max_length=255, example="F. Scott Fitzgerald")
    genre: str = Field(..., min_length=1, max_length=100, example="Classic")
    year_published: int = Field(..., ge=1000, le=9999, example=1925)  # Year should be a 4-digit number
    isbn: str = Field(..., min_length=10, max_length=13, pattern=r'^\d{10}(\d{3})?$', example="9780743273565")  # ISBN-10 or ISBN-13 format

    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate the ISBN format."""
        if not (len(v) == 10 or len(v) == 13):
            raise ValueError("ISBN must be 10 or 13 characters long.")
        return v
    
    @validator('year_published')
    def validate_year_published(cls, v):
        """Ensure the year_published is an integer within the valid range."""
        if not isinstance(v, int):
            raise ValueError("year_published must be an integer.")
        return v

    class Config:
        # To allow ORM mode if needed in future
        orm_mode = True

class BookUpdate(BaseModel):
    """Pydantic model for updating book details."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    year_published: Optional[int] = Field(None, ge=1000, le=9999)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13, pattern=r'^\d{10}(\d{3})?$')

    class Config:
        orm_mode = True
