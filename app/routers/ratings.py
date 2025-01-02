from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

# Create a rating for a book
@router.post("/{book_id}", response_model=schemas.Rating, status_code=201)
def create_rating(book_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    created_rating = crud.create_rating(db=db, rating=rating, book_id=book_id)
    if not created_rating:
        raise HTTPException(status_code=400, detail="Failed to create rating")
    return created_rating

# Get rating for a specific book
@router.get("/{book_id}", response_model=schemas.Rating)
def get_rating(book_id: int, db: Session = Depends(get_db)):
    db_rating = crud.get_rating(db=db, book_id=book_id)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

# Update the rating for a book
@router.put("/{rating_id}", response_model=schemas.Rating)
def update_rating(rating_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_rating = crud.update_rating(db=db, rating_id=rating_id, rating=rating)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

# Delete a rating for a book
@router.delete("/{rating_id}", response_model=None)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = crud.delete_rating(db=db, rating_id=rating_id)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return Response(status_code=204)
