from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

# ============================
# CRUD Operations for Books
# ============================

# **Create Operation**

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Books(
        title=book.title,
        author=book.author,
        genre=book.genre,
        publication_year=book.publication_year,
        status_reading=book.status_reading,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return schemas.BookResponse(
        id=db_book.id,
        title=db_book.title,
        author=db_book.author,
        genre=db_book.genre,
        publication_year=db_book.publication_year,
        status_reading=db_book.status_reading
    )


# **Read Operations**

def get_book(db: Session, book_id: int):
    return db.query(models.Books).filter(models.Books.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 99999):
    return db.query(models.Books).offset(skip).limit(limit).all()

# **Update Operation**
def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book:
        for key, value in book.model_dump(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

# **Delete Operation**
def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

# ============================
# CRUD Operations for Reading Progress
# ============================

def create_reading_progress(db: Session, progress: schemas.ReadingProgressCreate, book_id: int):
    db_progress = models.ReadingProgress(
        current_page=progress.current_page,
        total_pages=progress.total_pages,
        book_id=book_id,
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_reading_progress(db: Session, book_id: int):
    return db.query(models.ReadingProgress).filter(models.ReadingProgress.book_id == book_id).first()

def update_reading_progress(db: Session, progress_id: int, progress: schemas.ReadingProgressCreate):
    db_progress = db.query(models.ReadingProgress).filter(models.ReadingProgress.id == progress_id).first()
    if db_progress:
        for key, value in progress.model_dump(exclude_unset=True).items():
            setattr(db_progress, key, value)
        db.commit()
        db.refresh(db_progress)
    return db_progress

def delete_reading_progress(db: Session, progress_id: int):
    db_progress = db.query(models.ReadingProgress).filter(models.ReadingProgress.id == progress_id).first()
    if db_progress:
        db.delete(db_progress)
        db.commit()
    return db_progress

# ============================
# CRUD Operations for Notes
# ============================

def create_note(db: Session, note: schemas.NoteCreate, book_id: int):
    db_note = models.Note(
        notes_text=note.notes_text,
        book_id=book_id,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session, book_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Note).filter(models.Note.book_id == book_id).offset(skip).limit(limit).all()

def delete_note(db: Session, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note

# ============================
# CRUD Operations for Rating
# ============================

def create_rating(db: Session, rating: schemas.RatingCreate, book_id: int):
    db_rating = models.Rating(
        rating=rating.rating,
        user_feedback=rating.user_feedback,
        book_id=book_id,
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, book_id: int):
    return db.query(models.Rating).filter(models.Rating.book_id == book_id).first()

def update_rating(db: Session, rating_id: int, rating: schemas.RatingCreate):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if db_rating:
        for key, value in rating.model_dump(exclude_unset=True).items():
            setattr(db_rating, key, value)
        db.commit()
        db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return db_rating

# ============================
# CRUD Operations for Favorites
# ============================

def create_favorite(db: Session, favorite: schemas.FavoriteCreate, book_id: int):
    db_favorite = models.Favorite(is_favorite=favorite.is_favorite, book_id=book_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def get_favorite(db: Session, book_id: int):
    return db.query(models.Favorite).filter(models.Favorite.book_id == book_id).first()

def update_favorite(db: Session, favorite_id: int, favorite: schemas.FavoriteCreate):
    db_favorite = db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()
    if db_favorite:
        db_favorite.is_favorite = favorite.is_favorite
        db.commit()
        db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int):
    db_favorite = db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite
