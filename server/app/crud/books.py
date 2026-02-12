"""
Book data access operations.

Provides CRUD utilities and full-text cache lookup for Book records.
"""
from sqlalchemy.orm import Session
from app.models.book import Book
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from app.core.config import BOOK_CACHE_THRESHOLD

def get_book_by_title_and_authors(db: Session, title: str, authors: list[str]) -> Book | None:
    # title and authors must be normalized
    result = db.query(Book).filter(Book.normalized_title == title, Book.normalized_authors == authors).first()
    return result

def create_book(db: Session, book_data: dict) -> Book:
    """
    Create a new Book record.

    If a book with the same ISBN already exists, returns the existing record.
    This handles race conditions where multiple workers insert the same book.

    Args:
        db: Database session.
        book_data: Normalized book metadata.

    Returns:
        Created or existing Book.
    """
    book = Book(
        isbn_13=book_data.get("isbn_13"),
        title=book_data["title"],
        authors=book_data.get("authors", []),
        genres=book_data.get("genres", []),

        normalized_title=book_data["normalized_title"],
        normalized_authors=book_data.get("normalized_authors", []),
        search_key = book_data["normalized_title"] + " " + " ".join(book_data.get("normalized_authors", [])),

        language=book_data.get("language"),
        average_rating=book_data.get("average_rating"),
        ratings_count=book_data.get("ratings_count"),

        source=book_data["source"],
    )

    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        existing = db.query(Book).filter(Book.isbn_13 == book.isbn_13).first()
        return existing


def check_book_cache(session : Session, search_string: str) -> Book | None:
    """
    Perform full-text cache lookup using PostgreSQL ranking.

    Returns the best match only if its rank exceeds the threshold.

    Args:
        session: Database session.
        search_string: Normalized OCR text.

    Returns:
        Best matching Book or None if no strong match is found.
    """
    # full-text query and ranking expression
    ts_query = func.websearch_to_tsquery("english", search_string)
    rank_expr = func.ts_rank(Book.search_vector, ts_query)

    statement = (
        select(
            Book,
            rank_expr.label("rank")
        )
        .where(Book.search_vector.op("@@")(ts_query))
        .order_by(rank_expr.desc())
        .limit(1) # limiting to the row with the highest rank
    )

    result = session.execute(statement).first()
    
    if result is None:
        return None
    
    book, rank = result
    
    if rank < BOOK_CACHE_THRESHOLD: # checking the best result's rank compared to the threshold
            return None
    
    return book
    