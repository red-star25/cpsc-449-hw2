from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from pydantic_settings import BaseSettings

# Database Configuration Settings
class Settings(BaseSettings):
    DATABASE_URL: str = "mysql://username:password@localhost/bookdb"
    
    class Config:
        env_file = ".env"

# Create SQLAlchemy base and engine
settings = Settings()
Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy Book Model
class BookDB(Base):
    """
    Database model representing the book table in MySQL
    """
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    isbn = Column(String(13), unique=True)
    publication_year = Column(Integer)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models for Validation
class BookCreate(BaseModel):
    """
    Pydantic model for book creation validation
    """
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=13)
    publication_year: int = Field(..., gt=1000, le=datetime.now().year)
    price: float = Field(..., gt=0)
    is_available: bool = Optional[bool] = True
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Programming",
                "author": "John Smith",
                "isbn": "1234567890",
                "publication_year": 2023,
                "price": 49.99,
                "is_available": True
            }
        }
    )

class BookResponse(BaseModel):
    """
    Pydantic model for book response with ID
    """
    id: int
    title: str
    author: str
    isbn: str
    publication_year: int
    price: float
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)