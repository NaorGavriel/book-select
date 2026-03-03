from app.models.book import Book
from app.models.user_book import UserBook
from app.services.books.books import add_book
from app.crud.user_book import create_user_book, get_user_books
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def add_user_book(db: Session, title: str, author: str, user_id: int) -> UserBook | None:
    """
    Add a book to a user's reading history.

    Ensures the book exists in the system (creates it if necessary),
    then associates it with the given user.

    Args:
        db (Session): Active database session.
        title (str): Book title.
        author (str): Book author.
        user_id (int): Identifier of the user.

    Returns:
        UserBook : The created UserBook object or None if the book could not be resolved.
    """
    book = add_book(db, title, author)

    if book is None:
        return None # will return error
    
    book_user = {
        "user_id":user_id,
        "book_id":book.id
    }

    result = create_user_book(db=db, book_user_data=book_user)

    return result


def get_books_of_user(db: Session, user_id : int) -> list[Book]:
    try :
        books = get_user_books(db=db, user_id=user_id)
        return books
    except IntegrityError:
        return []