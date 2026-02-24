
from sqlalchemy.orm import Session
from app.models.user_book import UserBook
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.book import Book
from app.models.user_book import UserBook

def create_user_book(db: Session, book_user_data : dict) -> UserBook:
    book_user = UserBook(
        user_id=book_user_data.get("user_id"),
        book_id=book_user_data.get("book_id")
    )

    try:
        db.add(book_user)
        db.commit()
        db.refresh(book_user)
        return book_user
    except IntegrityError:
        db.rollback()
        existing = db.query(UserBook).filter(UserBook.user_id == book_user.user_id, UserBook.book_id == book_user.book_id).first()
        return existing
    

def get_user_books(db: Session, user_id: int) -> list[Book]:
    """
    Retrieve all books associated with a given user.
    """

    stmt = (
        select(Book)
        .join(UserBook, UserBook.book_id == Book.id)
        .where(UserBook.user_id == user_id)
    )

    result = db.execute(stmt).scalars().all()

    return result