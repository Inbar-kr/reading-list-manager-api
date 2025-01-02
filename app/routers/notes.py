from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db

router = APIRouter()

# Create a note for a book
@router.post("/{book_id}", response_model=schemas.Note, status_code=201)
def create_note(book_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_note(db=db, note=note, book_id=book_id)

# Get notes for a specific book
@router.get("/{book_id}", response_model=schemas.NotesResponse)
def get_notes(book_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    notes = crud.get_notes(db=db, book_id=book_id, skip=skip, limit=limit)
    return {"notes": notes}

# Delete a note for a book
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.delete_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=204)
