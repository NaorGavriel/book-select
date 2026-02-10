from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base

class Book(Base):
    """
    Cached book metadata sourced from external APIs.

    This table is treated as a read-optimized cache, not a fully normalized
    publishing database.
    """
    
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


    isbn_13: Mapped[str] = mapped_column(String, unique=True, nullable=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    authors: Mapped[list[str]] = mapped_column(JSONB)
    genres: Mapped[list[str]] = mapped_column(JSONB)

    normalized_title: Mapped[list[str]] = mapped_column(String, index=True)
    normalized_authors: Mapped[list[str]] = mapped_column(JSONB)


    language: Mapped[str | None] = mapped_column(String, nullable=True)
    average_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    ratings_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    source: Mapped[str] = mapped_column(String)
    """Source of the metadata"""

    last_updated: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
