# models.py

from sqlalchemy import Column, Date, Integer, String

from .database import Base


# Define the Book model
class Book(Base):
    __tablename__ = "books"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    published_date = Column(Date, nullable=True)
    genre = Column(String(100), nullable=True)
    
    # Add more fields as necessary
