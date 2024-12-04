from fastapi import FastAPI, HTTPException

from database import create_connection
from models import Book, BookUpdate

app = FastAPI()

@app.post("/books/")
async def create_book(book: Book):
    try:
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # This handles invalid values


@app.get("/books/")
async def get_all_books():
    """Retrieve all books."""
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    query = "SELECT * FROM books"
    cursor.execute(query)
    result = cursor.fetchall()
    
    books = []
    for row in result:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "year_published": row[4],
            "isbn": row[5]
        })
    
    cursor.close()
    connection.close()
    
    return {"books": books}

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
