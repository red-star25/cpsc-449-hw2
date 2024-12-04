from typing import List

# Import previous database configuration and models
from database_config import (Base, BookCreate, BookDB, BookResponse,
                             SessionLocal, engine)
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# Create FastAPI application
app = FastAPI(
    title="Book Management System",
    description="A comprehensive book management API with MySQL backend",
    version="1.0.0"
)

# Database Dependency
def get_db():
    """
    Create and return a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# CRUD Operations

@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the database
    """
    # Check if ISBN already exists
    existing_book = db.query(BookDB).filter(BookDB.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")
    
    # Create book DB model
    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of books with optional pagination
    """
    books = db.query(BookDB).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific book by its ID
    """
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """
    Update an existing book's details
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database
    """
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return None

# Search and Filter Endpoints

@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = None, 
    author: Optional[str] = None, 
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Advanced search for books with multiple filter options
    """
    query = db.query(BookDB)
    
    if title:
        query = query.filter(BookDB.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.filter(BookDB.price >= min_price)
    if max_price is not None:
        query = query.filter(BookDB.price <= max_price)
    
    return query.all()

# Main run configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)