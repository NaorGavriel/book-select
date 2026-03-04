
from app.models.book import Book
from app.services.books.google_books import extract_book_data, search_google_books
from app.services.openai.openai_embedding import generate_embedding
from app.crud.books import check_book_cache, create_book
from app.utils.text import normalize_text
from sqlalchemy.orm import Session
import logging 
from app.core.config import GeneralConfig

logger = logging.getLogger(GeneralConfig.API_LOGGER_NAME)

def add_book(db : Session ,title : str, author : str) -> Book | None :
    """
    Retrieve or create a Book entity.

    Args:
        db (Session): Active database session.
        title (str).
        author (str).

    Returns:
        Book: Existing or newly created Book, or None if no external match was found.
    """
    title_normalized = normalize_text(title)
    author_normalized = normalize_text(author)
    normalized_text = title + ' ' + author # Normalize input

    book_match : Book | None = check_book_cache(session=db, search_string=normalized_text)
    
    if book_match is None:
        
        # Fallback to external search when cache miss occurs
        book_candidate = search_google_books(search_term=normalized_text, title=title_normalized, author=author_normalized)

        if book_candidate is None: # no relevant result returned from google books api
            return None

        book_data = extract_book_data(book_candidate) # transforming API response to internal schema
        book_embedding = generate_embedding(book_data.get("description"))
        book_data["embedding"] = book_embedding
        book_match = create_book(db=db, book_data=book_data) # adding the new book to the database
    
    if book_match is not None:
        logger.info("user added book")

    return book_match
