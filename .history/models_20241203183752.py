from pydantic import BaseModel, validator


class Book(BaseModel):
    """Pydantic model to represent a Book."""
    title: str
    author: str
    genre: str
    year_published: int
    isbn: str

    @validator('isbn')
    def validate_isbn(cls, v):
        if not v.isdigit() or len(v) != 13:
            raise ValueError("Invalid ISBN format (must be 13 digits)")
        return v

class BookUpdate(BaseModel):
    """Pydantic model for updating book details."""
    title: str = None
    author: str = None
    genre: str = None
    year_published: int = None
    isbn: str = None