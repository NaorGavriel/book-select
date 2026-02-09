from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base


class Preferences(Base):
    """
    Per-user preference configuration used for recommendation scoring.

    Stored as weighted values to allow flexible, explainable matching logic.
    """

    __tablename__ = "user_preferences"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    genres: Mapped[dict[str, float]] = mapped_column(JSONB, default=dict)
    authors: Mapped[dict[str, float]] = mapped_column(JSONB, default=dict)
    excluded_books: Mapped[list[str]] = mapped_column(JSONB, default=dict)

    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="preferences")
