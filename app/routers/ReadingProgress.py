from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

# Create reading progress for a book
@router.post("/{book_id}", response_model=schemas.ReadingProgress, status_code=status.HTTP_201_CREATED)
def create_reading_progress(book_id: int, progress: schemas.ReadingProgressCreate, db: Session = Depends(get_db)):
    return crud.create_reading_progress(db=db, book_id=book_id, progress=progress)

# Get reading progress for a specific book
@router.get("/{book_id}", response_model=schemas.ReadingProgress)
def get_reading_progress(book_id: int, db: Session = Depends(get_db)):
    db_progress = crud.get_reading_progress(db=db, book_id=book_id)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return db_progress

# Update reading progress
@router.put("/{progress_id}", response_model=schemas.ReadingProgress)
def update_reading_progress(progress_id: int, progress: schemas.ReadingProgressCreate, db: Session = Depends(get_db)):
    db_progress = crud.update_reading_progress(db=db, progress_id=progress_id, progress=progress)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return db_progress

# Delete reading progress
@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading_progress(progress_id: int, db: Session = Depends(get_db)):
    db_progress = crud.delete_reading_progress(db=db, progress_id=progress_id)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return None