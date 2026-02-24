"""
Book resolution service.

Attempts to resolve OCR-detected book strings using the local cache.
If no suitable match is found, falls back to Google Books and stores the result.
"""
from sqlalchemy.orm import Session
from app.models.book import Book
from app.services.books.google_books import search_google_books, extract_book_data
from app.crud.books import create_book, check_book_cache
from app.services.openai.openai_embedding import generate_embedding
from app.utils.text import normalize_text

def resolve_books(db: Session, detected_books: list[str]) -> list[Book]:
    """
    Resolve a list of detected book strings to Book records.

    For each detected string:
    1. Normalize text for consistent searching.
    2. Attempt cache lookup using full-text search.
    3. If not found, query Google Books and persist the result.

    Args:
        db: Active database session.
        detected_books: OCR-extracted book strings.

    Returns:
        List of resolved Book objects (cache hits and newly created).
    """
    resolved = []

    for detected_book in detected_books:
        # Normalize OCR text to improve cache matching consistency
        normalized_text = normalize_text(detected_book)
        
        book_match : Book | None = check_book_cache(session=db, search_string=normalized_text)

        if book_match is None:
            # Fallback to external search when cache miss occurs
            book_candidate = search_google_books(normalized_text)

            if book_candidate is None: # no relevant result returned from google books api
                continue

            
            book_data = extract_book_data(book_candidate) # transforming API response to internal schema
            book_embedding = generate_embedding(book_data.get("description"))
            book_data["embedding"] = book_embedding
            book_match = create_book(db=db, book_data=book_data) # adding the new book to the database
        
        resolved.append(book_match)

    return resolved

