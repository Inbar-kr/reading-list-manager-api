from fastapi import APIRouter
from app.routers import books, ReadingProgress, notes, ratings, favorites

router = APIRouter()

router.include_router(books.router, prefix="/books", tags=["Books"])
router.include_router(ReadingProgress.router, prefix="/progress", tags=["Reading Progress"])
router.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
