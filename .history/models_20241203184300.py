import re
from typing import Optional

from pydantic import BaseModel, root_validator, validator


class Book(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    isbn: str

    @validator("year_published")
    def check_year(cls, value):
        if value < 0 or value > 2024:
            raise ValueError("Year must be between 0 and 2024.")
        return value

    @validator("isbn")
    def check_isbn(cls, value):
        # Validate ISBN format (simple check for length and numbers)
        if not re.match(r"^\d{3}-\d{10}$", value):
            raise ValueError("Invalid ISBN format. Example: 123-1234567890")
        return value


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    isbn: Optional[str] = None

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(value is not None for value in values.values()):
            raise ValueError("At least one field must be provided for update.")
        return values

    @validator("year_published", always=True)
    def check_year_update(cls, value):
        if value is not None and (value < 0 or value > 2024):
            raise ValueError("Year must be between 0 and 2024.")
        return value

    @validator("isbn", always=True)
    def check_isbn_update(cls, value):
        if value and not re.match(r"^\d{3}-\d{10}$", value):
            raise ValueError("Invalid ISBN format. Example: 123-1234567890")
        return value
