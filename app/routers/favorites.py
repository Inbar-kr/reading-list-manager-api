from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db

router = APIRouter()

# Mark a book as favorite
@router.post("/{book_id}", response_model=schemas.Favorite, status_code=status.HTTP_201_CREATED)
def create_favorite(book_id: int, favorite: schemas.FavoriteCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    created_favorite = crud.create_favorite(db=db, favorite=favorite, book_id=book_id)
    return created_favorite


# Get favorite status for a book
@router.get("/{book_id}", response_model=schemas.Favorite)
def get_favorite(book_id: int, db: Session = Depends(get_db)):
    db_favorite = crud.get_favorite(db=db, book_id=book_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite status not found")
    return db_favorite

# Update favorite status for a book
@router.put("/{favorite_id}", response_model=schemas.Favorite)
def update_favorite(favorite_id: int, favorite: schemas.FavoriteCreate, db: Session = Depends(get_db)):
    db_favorite = crud.update_favorite(db=db, favorite_id=favorite_id, favorite=favorite)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite status not found")
    return db_favorite

# Delete favorite status for a book
@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = crud.delete_favorite(db=db, favorite_id=favorite_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite status not found")
    return None
