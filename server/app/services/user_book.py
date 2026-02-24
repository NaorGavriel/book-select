from app.models.book import Book
from app.services.books.books import add_book
from app.crud.user_book import create_user_book
from sqlalchemy.orm import Session

def add_user_book(db: Session, title: str, author: str, user_id: int) -> Book | None:
    book = add_book(db, title, author)

    if book is None:
        return None # will return error
    
    book_user = {
        "user_id":user_id,
        "book_id":book.id
    }

    result = create_user_book(db=db, book_user_data=book_user)

    return result