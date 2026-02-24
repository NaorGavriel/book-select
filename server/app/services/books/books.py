
from app.models.book import Book
from app.services.books.google_books import extract_book_data, search_google_books
from app.crud.books import check_book_cache, create_book
from app.utils.text import normalize_text
from sqlalchemy.orm import Session

def add_book(db : Session ,title : str, author : str) -> Book | None :
    normalized_text = normalize_text(title + ' ' + author)

    book_match : Book | None = check_book_cache(session=db, search_string=normalized_text)

    if book_match is None:
        # Fallback to external search when cache miss occurs
        book_candidate = search_google_books(normalized_text)

        if book_candidate is None: # no relevant result returned from google books api
            return None

        book_data = extract_book_data(book_candidate) # transforming API response to internal schema
        book_match = create_book(db=db, book_data=book_data) # adding the new book to the database
        
    return book_match
