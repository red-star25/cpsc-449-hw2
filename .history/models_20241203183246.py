from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    isbn: str

class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    genre: str = None
    year_published: int = None
    isbn: str = None
