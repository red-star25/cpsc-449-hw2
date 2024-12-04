# crud.py
from sqlalchemy.orm import Session

from .models import Book
from .schemas import Book, BookCreate


# Create a new book
def create_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        author=book.author,
        published_date=book.published_date,
        genre=book.genre
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Get all books
def get_books(db: Session):
    return db.query(Book).all()

# Get a specific book by ID
def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

# Update a book by ID
def update_book(db: Session, book_id: int, book: BookCreate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.published_date = book.published_date
        db_book.genre = book.genre
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

# Delete a book by ID
def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None
