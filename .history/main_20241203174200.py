from fastapi import FastAPI, HTTPException

from database import create_connection
from models import Book, BookUpdate

app = FastAPI()

@app.post("/books/")
async def create_book(book: Book):
    """Create a new book record."""
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    query = """INSERT INTO books (title, author, genre, year_published, isbn) 
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (book.title, book.author, book.genre, book.year_published, book.isbn))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Book added successfully"}
    

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    """Retrieve a book by its ID."""
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    query = "SELECT * FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()
    
    if result:
        return {"id": result[0], "title": result[1], "author": result[2], "genre": result[3], "year_published": result[4], "isbn": result[5]}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookUpdate):
    """Update a book record."""
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    query = """UPDATE books SET title = %s, author = %s, genre = %s, 
               year_published = %s, isbn = %s WHERE id = %s"""
    cursor.execute(query, (book.title, book.author, book.genre, book.year_published, book.isbn, book_id))
    connection.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    cursor.close()
    connection.close()
    return {"message": "Book updated successfully"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book record."""
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    query = "DELETE FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    connection.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    cursor.close()
    connection.close()
    return {"message": "Book deleted successfully"}
