from pydantic import BaseModel


class Book(BaseModel):
    """Pydantic model to represent a Book."""
    title: str
    author: str
    genre: str
    year_published: int
    isbn: str

class BookUpdate(BaseModel):
    """Pydantic model for updating book details."""
    title: str = None
    author: str = None
    genre: str = None
    year_published: int = None
    isbn: str = None
