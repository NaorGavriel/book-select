from sqlalchemy.orm import Session
from app.models.book import Book
from app.services.books.google_books import search_google_books, extract_book_data, filter_books
from app.crud.books import get_book_by_title_and_authors, create_book
from app.services.books.utils import normalize_authors, normalize_title

def resolve_books(db: Session, detected_books: list[dict]) -> list[Book]:

    resolved = []

    for detected_book in detected_books:
        # normalizing title and authors to search the DB
        normalized_title = normalize_title(detected_book["title"])
        normalized_authors = normalize_authors(detected_book["authors"])

        book = get_book_by_title_and_authors(db, normalized_title, normalized_authors)

        if book : # book found, appending relevant book data
            resolved.append(book)
            continue

        authors = detected_book.get("authors", [])
        author = authors[0] if authors else None

        book_api_results = search_google_books(title=detected_book["title"], author=author)
        book_match = filter_books(normalized_title=normalized_title, candidates=book_api_results)

        if book_match is None:
            continue

        # extracting relevant book data to persist in database
        book_data = extract_book_data(book_match)
        new_book_entry = create_book(db=db, book_data=book_data)
        resolved.append(new_book_entry)

    return resolved
