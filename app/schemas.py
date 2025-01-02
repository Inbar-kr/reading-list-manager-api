from pydantic import BaseModel, model_validator,Field, field_validator
from typing import List, Optional
from enum import Enum
from datetime import datetime, timezone
from fastapi import HTTPException, status

# Enum for Reading Status
class ReadingStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    publication_year: Optional[int] = None
    status_reading: ReadingStatus

    class ConfigDict:
        use_enum_values = True


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class ConfigDict:
        use_enum_values = True


class BookUpdate(BookBase):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    publication_year: Optional[int]
    status_reading: Optional[ReadingStatus]

    class ConfigDict:
        from_attributes = True


class ReadingProgressBase(BaseModel):
    current_page: int
    total_pages: int


class ReadingProgressCreate(ReadingProgressBase):
    @model_validator(mode="before")
    def validate_current_page(cls, values):
        current_page = values.get('current_page')
        total_pages = values.get('total_pages')
        if current_page < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="current_page cannot be negative"
            )
        if total_pages is not None and current_page > total_pages:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="current_page cannot be greater than total_pages"
            )
        return values

class ReadingProgress(ReadingProgressBase):
    id: int
    book_id: int
    percentage_completed: float

    class ConfigDict:
        from_attributes = True


class NoteBase(BaseModel):
    notes_text: str
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class NoteCreate(NoteBase):
    @field_validator('notes_text')
    def check_notes_text_not_empty(cls, v):
        if not v.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Notes text cannot be empty"
            )
        return v


class Note(NoteBase):
    id: int
    book_id: int

    class ConfigDict:
        from_attributes = True


class RatingBase(BaseModel):
    rating: int
    user_feedback: Optional[str] = None

    @field_validator("rating")
    def validate_rating(cls, value):
        if value < 1 or value > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
        return value


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    book_id: int

    class ConfigDict:
        from_attributes = True


class FavoriteBase(BaseModel):
    is_favorite: bool


class FavoriteCreate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: int
    book_id: int

    class ConfigDict:
        from_attributes = True


# Response Schemas
class BooksResponse(BaseModel):
    books: List[BookBase]


class ReadingProgressResponse(BaseModel):
    progress: List[ReadingProgress]


class NotesResponse(BaseModel):
    notes: List[Note]


class RatingsResponse(BaseModel):
    ratings: List[Rating]


class FavoritesResponse(BaseModel):
    favorites: List[Favorite]
