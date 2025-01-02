from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from app.database import Base
from app.schemas import ReadingStatus

class Books(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), unique=True, nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    publication_year = Column(Integer)
    status_reading = Column(SQLAlchemyEnum(ReadingStatus, native_enum=False, use_enum_values=True),
                            default=ReadingStatus.not_started)

    # Relationships
    progress = relationship("ReadingProgress", back_populates="book", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="book", cascade="all, delete-orphan")
    rating = relationship("Rating", back_populates="book", cascade="all, delete-orphan")
    favorite = relationship("Favorite", back_populates="book", uselist=False)


class ReadingProgress(Base):
    __tablename__ = "ReadingProgress"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)
    current_page = Column(Integer, default=0, nullable=False)
    total_pages = Column(Integer, nullable=False)

    # Relationships
    book = relationship("Books", back_populates="progress")

    @property
    def percentage_completed(self):
        if self.total_pages == 0:
            return 0.0
        return (self.current_page / self.total_pages) * 100

class Note(Base):
    __tablename__ = "Notes"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)
    notes_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=None)

    # Relationships
    book = relationship("Books", back_populates="notes")

class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    user_feedback = Column(Text, nullable=True)

    # Relationships
    book = relationship("Books", back_populates="rating")

    def set_rating(self, value: int):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = value

    @property
    def get_rating(self):
        return self.rating


class Favorite(Base):
    __tablename__ = "Favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)
    is_favorite = Column(Boolean, default=False)

    # Relationships
    book = relationship("Books", back_populates="favorite")

