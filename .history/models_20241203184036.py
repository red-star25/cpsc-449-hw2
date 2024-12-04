from pydantic import BaseModel, Field, ValidationError


class Book(BaseModel):
    """Pydantic model to represent a Book."""
    title: str
    author: str
    genre: str
    year_published: int = Field(..., gt=0)  # Enforce positive integer

    @validator('year_published')
    def validate_year_published(cls, v):
        if not isinstance(v, int):
            raise ValidationError('year_published must be an integer')
        return v

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