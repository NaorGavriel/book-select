
from sqlalchemy.orm import Session
from app.models.user_book import UserBook
from sqlalchemy.exc import IntegrityError


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