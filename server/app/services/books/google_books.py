"""
Google Books integration.

Handles:
- Query construction
- External API requests
- Result filtering
- Data transformation into internal format
"""
import httpx
from app.utils.text import normalize_authors, normalize_title, normalize_text
import logging
from app.core.config.config import settings

MAX_DESCRIPTION_LENGTH = 1000
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

if not settings.GOOGLE_BOOKS_API_KEY:
    raise RuntimeError("GOOGLE_BOOKS_API_KEY not found")

logger = logging.getLogger(settings.API_LOGGER_NAME)

def search_google_books(
    search_term: str = None,
    title: str = None,
    author: str = None,
):
    """
    Query Google Books and return the best matching result.

    Returns:
        A single volume dict or None if no valid result is found.
    """
    query = _build_query(search_term, title, author)
    if query is None:
        return None

    items = _fetch_books(query)
    return filter_results(items, author)


def _build_query(search_term: str, title: str, author: str) -> str | None:
    """Construct query string for Google Books API."""
    if title and author:
        return f'intitle:"{title}" inauthor:"{author}"'
    return search_term

def _fetch_books(query: str) -> list[dict]:
    """Fetch raw results from Google Books API."""
    params = {
        "q": query,
        "langRestrict": "en",
        "maxResults": settings.GOOGLE_BOOKS_MAX_RESULTS,
        "key": settings.GOOGLE_BOOKS_API_KEY,
    }

    with httpx.Client(timeout=5.0) as client:
        logger.info("google books api call")
        resp = client.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    return data.get("items", [])

def extract_book_data(item: dict) -> dict:
    """
    Extract and normalize relevant fields from a Google Books volume.

    Args:
        item: Volume item from Google Books API.

    Returns:
        Dictionary formatted for Book creation.
    """

    v = item.get("volumeInfo", {})

    isbn_13 = None
    for identifier in v.get("industryIdentifiers", []):
        if identifier.get("type") == "ISBN_13":
            isbn_13 = identifier.get("identifier")
            break

    title = v.get("title")
    authors = v.get("authors") or []
    description = v.get("description")
    genres = v.get("categories", [])

    if description and len(description) > MAX_DESCRIPTION_LENGTH: # truncating long descriptions
        description = description[:MAX_DESCRIPTION_LENGTH]

    book_data = {
        "isbn_13": isbn_13,
        "title": title,
        "authors": authors,
        "genres": genres,
        "normalized_title": normalize_title(title),
        "normalized_authors": normalize_authors(authors),
        "description": description,
        "language": v.get("language"),
        "average_rating": v.get("averageRating"),
        "ratings_count": v.get("ratingsCount"),
        "source": "google_books",
    }

    return book_data

def filter_results(items: list[dict], author : str = None) -> list[dict]:
    """
    Filters Google Books API results, keeps the most relevant book in english that includes these features:
        - description
        - title
        - author
    """
    filtered = []

    for item in items:
        volume_info = item.get("volumeInfo", {})
        
        if (
            volume_info.get("language") == "en"
            and volume_info.get("description")
            and volume_info.get("title")
            and volume_info.get("authors")
            
        ):
            if author:
                candidate_authors = " ".join(volume_info.get("authors", []))
                candidate_authors_normalized = normalize_text(candidate_authors)
                if author in candidate_authors_normalized:
                    filtered.append(item)
            else :
                filtered.append(item)

    return filtered[0] if filtered else None
