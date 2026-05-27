"""
Book resolution service.

Attempts to resolve OCR-detected book strings using the local cache.
If no suitable match is found, falls back to Google Books and stores the result.
"""
import logging
import time

from sqlalchemy.orm import Session

from app.core.config.config import settings
from app.core.redis_client import get_redis_client
from app.crud.books import check_book_cache, create_book
from app.models.book import Book
from app.services.books.google_books import extract_book_data, search_google_books
from app.services.openai.openai_embedding import generate_embedding
from app.utils.text import normalize_text

logger = logging.getLogger(settings.API_LOGGER_NAME)

_redis = get_redis_client()

def resolve_books(db: Session, detected_books: list[str]) -> list[Book] | None:
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

    logger.info(f"Resolving {len(detected_books)} detected books")

    for detected_book in detected_books:
        # Normalize OCR text to improve cache matching consistency
        normalized_text = normalize_text(detected_book)
        
        _start = time.perf_counter()
        book_match : Book | None = check_book_cache(session=db, search_string=normalized_text)
        _elapsed_ms = (time.perf_counter() - _start) * 1000

        try:
            _redis.incr("metrics:cache:hits" if book_match else "metrics:cache:misses")
            _redis.incrbyfloat("metrics:cache:lookup_latency_ms_sum", _elapsed_ms)
            _redis.incr("metrics:cache:lookup_count")
        except Exception:
            pass  # metrics failure must never block book resolution

        if book_match:
            logger.info(f"Cache hit for '{normalized_text}'")
        else:
            logger.info(f"Cache miss for '{normalized_text}'")
            # Fallback to external search when cache miss occurs
            try :
                book_candidate = search_google_books(normalized_text)
            
                if book_candidate is None: # no relevant result returned from google books api
                    logger.info(f"No Google Books result for '{normalized_text}'")
                    continue

                
                book_data = extract_book_data(book_candidate) # transforming API response to internal schema
                book_embedding = generate_embedding(book_data.get("description"))
                book_data["embedding"] = book_embedding
                book_match = create_book(db=db, book_data=book_data) # adding the new book to the database
            except Exception as e:
                logger.exception("Failed resolving book", extra={"book": normalized_text})
                continue
        

        resolved.append(book_match)

    logger.info(f"Resolved {len(resolved)} books")
    if not resolved:
        return None
    
    return resolved

