from fastapi import FastAPI, HTTPException

from database import create_connection
from models import Book, BookUpdate

app = FastAPI() # Creating a FastAPI instance

@app.post("/books/")  # Route to handle POST requests for adding a new book
async def create_book(book: Book):  # The function to create a new book. The book data is validated using the Book model.
    try:
        connection = create_connection()  # Establishing a connection to the database
        if not connection:  # Checking if the connection was successful
            raise HTTPException(status_code=500, detail="Database connection failed")  # Raising an error if connection failed

        cursor = connection.cursor()  # Creating a cursor object to execute SQL queries
        query = """INSERT INTO books (title, author, genre, year_published, isbn) 
                   VALUES (%s, %s, %s, %s, %s)"""  # SQL query to insert a new book into the 'books' table
        cursor.execute(query, (book.title, book.author, book.genre, book.year_published, book.isbn))  # Executing the query with book data
        connection.commit()  # Committing the transaction to save the changes
        cursor.close()  # Closing the cursor
        connection.close()  # Closing the database connection
        return {"message": "Book added successfully"}  # Returning a success message
    except ValueError as e:  # Handling any validation errors
        raise HTTPException(status_code=400, detail=str(e))  # Raising an HTTP 400 error with the exception message


@app.get("/books/")  # Route to handle GET requests for retrieving all books
async def get_all_books():  # Function to fetch all books from the database
    connection = create_connection()  # Establishing a connection to the database
    if not connection:  # Checking if the connection was successful
        raise HTTPException(status_code=500, detail="Database connection failed")  # Raising an error if connection failed
    
    cursor = connection.cursor()  # Creating a cursor object to execute SQL queries
    query = "SELECT * FROM books"  # SQL query to select all records from the 'books' table
    cursor.execute(query)  # Executing the query to fetch all books
    result = cursor.fetchall()  # Fetching all the results from the query
    
    books = []  # List to store book data in dictionary format
    for row in result:  # Iterating through each row in the result
        books.append({
            "id": row[0],  # Mapping the 'id' from the database result
            "title": row[1],  # Mapping the 'title' from the database result
            "author": row[2],  # Mapping the 'author' from the database result
            "genre": row[3],  # Mapping the 'genre' from the database result
            "year_published": row[4],  # Mapping the 'year_published' from the database result
            "isbn": row[5]  # Mapping the 'isbn' from the database result
        })
    
    cursor.close()  # Closing the cursor
    connection.close()  # Closing the database connection
    
    return {"books": books}  # Returning the list of all books


@app.get("/books/{book_id}")  # Route to handle GET requests for retrieving a book by its ID
async def get_book(book_id: int):  # Function to fetch a single book by its ID
    connection = create_connection()  # Establishing a connection to the database
    if not connection:  # Checking if the connection was successful
        raise HTTPException(status_code=500, detail="Database connection failed")  # Raising an error if connection failed
    
    cursor = connection.cursor()  # Creating a cursor object to execute SQL queries
    query = "SELECT * FROM books WHERE id = %s"  # SQL query to select a book by its ID
    cursor.execute(query, (book_id,))  # Executing the query with the provided book_id
    result = cursor.fetchone()  # Fetching the first result
    
    if result:  # If a result is found, return the book data
        return {"id": result[0], "title": result[1], "author": result[2], "genre": result[3], "year_published": result[4], "isbn": result[5]}
    else:  # If no result is found
        raise HTTPException(status_code=404, detail="Book not found")  # Raising an HTTP 404 error indicating that the book does not exist


@app.put("/books/{book_id}")  # Route to handle PUT requests for updating a book
async def update_book(book_id: int, book: BookUpdate):  # Function to update a book using the BookUpdate model for validation
    connection = create_connection()  # Establishing a connection to the database
    if not connection:  # Checking if the connection was successful
        raise HTTPException(status_code=500, detail="Database connection failed")  # Raising an error if connection failed
    
    cursor = connection.cursor()  # Creating a cursor object to execute SQL queries
    query = """UPDATE books SET title = %s, author = %s, genre = %s, 
               year_published = %s, isbn = %s WHERE id = %s"""  # SQL query to update the book with the new data
    cursor.execute(query, (book.title, book.author, book.genre, book.year_published, book.isbn, book_id))  # Executing the update query
    connection.commit()  # Committing the transaction to save the changes
    
    if cursor.rowcount == 0:  # If no rows were updated, the book does not exist
        raise HTTPException(status_code=404, detail="Book not found")  # Raising an HTTP 404 error indicating the book was not found
    
    cursor.close()  # Closing the cursor
    connection.close()  # Closing the database connection
    return {"message": "Book updated successfully"}  # Returning a success message


@app.delete("/books/{book_id}")  # Route to handle DELETE requests for deleting a book by its ID
async def delete_book(book_id: int):  # Function to delete a book by its ID
    connection = create_connection()  # Establishing a connection to the database
    if not connection:  # Checking if the connection was successful
        raise HTTPException(status_code=500, detail="Database connection failed")  # Raising an error if connection failed
    
    cursor = connection.cursor()  # Creating a cursor object to execute SQL queries
    query = "DELETE FROM books WHERE id = %s"  # SQL query to delete a book by its ID
    cursor.execute(query, (book_id,))  # Executing the delete query
    connection.commit()  # Committing the transaction to delete the book
    
    if cursor.rowcount == 0:  # If no rows were deleted, the book does not exist
        raise HTTPException(status_code=404, detail="Book not found")  # Raising an HTTP 404 error indicating the book was not found
    
    cursor.close()  # Closing the cursor
    connection.close()  # Closing the database connection
    return {"message": "Book deleted successfully"}  # Returning a success message
