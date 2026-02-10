from sqlalchemy.orm import Session
from app.models.book import Book

def get_book_by_title_and_authors(db: Session, title: str, authors: list[str]) -> Book | None:
    # title and authors must be normalized
    result = db.query(Book).filter(Book.normalized_title == title, Book.normalized_authors == authors).first()
    return result
