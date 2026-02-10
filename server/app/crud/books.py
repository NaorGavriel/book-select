from sqlalchemy.orm import Session
from app.models.book import Book

def get_book_by_title_and_authors(db: Session, title: str, authors: list[str]) -> Book | None:
    # title and authors must be normalized
    result = db.query(Book).filter(Book.normalized_title == title, Book.normalized_authors == authors).first()
    return result

def create_book(db: Session, book_data: dict) -> Book:
    book = Book(
        isbn_13=book_data.get("isbn_13"),
        title=book_data["title"],
        authors=book_data.get("authors", []),
        genres=book_data.get("genres", []),

        normalized_title=book_data["normalized_title"],
        normalized_authors=book_data.get("normalized_authors", []),

        language=book_data.get("language"),
        average_rating=book_data.get("average_rating"),
        ratings_count=book_data.get("ratings_count"),

        source=book_data["source"],
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book
    