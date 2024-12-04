from pydantic import BaseModel, constr


class Book(BaseModel):
    title: constr(min_length=1, max_length=255)  # Enforce title length limits
    author: constr(min_length=1, max_length=255)  # Enforce author name length limits
    genre: constr(min_length=1, max_length=100)  # Enforce genre length limits
    year_published: int  # Year should be an integer
    isbn: constr(regex=r"^\d{13}$")  # Validate ISBN format (13 digits)

class BookUpdate(BaseModel):
    title: constr(min_length=1, max_length=255, optional=True)
    author: constr(min_length=1, max_length=255, optional=True)
    genre: constr(min_length=1, max_length=100, optional=True)
    year_published: int = None  # Allow None for optional update
    isbn: constr(regex=r"^\d{13}$", optional=True)  # Optional ISBN update