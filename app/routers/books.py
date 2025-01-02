from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from typing import List, Optional

router = APIRouter()

# Create a new book
@router.post("/", response_model=schemas.BookResponse, status_code=201)
def create_book_endpoint(book: schemas.BookCreate, db: Session = Depends(get_db)):
    created_book = crud.create_book(db=db, book=book)
    if not created_book:
        raise HTTPException(status_code=400, detail="Failed to create book")
    return created_book

# Get a specific book by ID
@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Get a list of books
@router.get("/", response_model=schemas.BooksResponse)
def get_books(skip: int = 0, limit: int = 99999, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return {"books": books}

# Update a book
@router.put("/{book_id}", response_model=schemas.BookBase)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = crud.update_book(db=db, book_id=book_id, book=book)
    return updated_book

# Delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

"""# Fetch Books with Progress, Notes, and Ratings
@router.get("/{book_id}", response_model=schemas.BookDetailsResponse)
def get_book_details(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book_details(db=db, book_id=book_id)

# Filter Books Dynamically
@router.get("/books/filter", response_model=List[schemas.BookResponse])
def filter_books(genre: Optional[str] = None, author: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.filter_books(db, genre, author, status)"""
