from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.models.base import Base

class UserBook(Base):
    """
    Association table linking users and books (many-to-many).
    Represents a book that a specific user has added to their reading history.
    """
    __tablename__ = "user_books"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("books.id"),
        primary_key=True
    )