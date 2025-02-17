# Book Management System

## Overview

A comprehensive Book Management System built with FastAPI and MySQL, providing CRUD operations and advanced search capabilities.

## Features

- Create, Read, Update, Delete (CRUD) book operations
- Advanced book search with multiple filters
- Input validation using Pydantic
- MySQL database integration

## Prerequisites

- Python 3.9+
- MySQL Server
- pip package manager

## Installation Steps

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `uvicorn main:app --reload`

## API Endpoints

- `POST /books/`: Create a new book
- `GET /books/`: List all books
- `GET /books/{book_id}`: Get a specific book
- `PUT /books/{book_id}`: Update a book
- `DELETE /books/{book_id}`: Delete a book
