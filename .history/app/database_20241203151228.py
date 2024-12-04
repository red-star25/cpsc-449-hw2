# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL: Modify with your database credentials
DATABASE_URL = "mysql+mysqlconnector://<username>:<password>@localhost:3306/book_management_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()