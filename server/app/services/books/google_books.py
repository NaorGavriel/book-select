"""
Google Books integration.

Handles external search requests and transforms API responses
into the internal book data format.
"""
import httpx
from app.core.config import GOOGLE_BOOKS_API_KEY, MAX_RESULTS
from app.utils.text import normalize_authors, normalize_title

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

if not GOOGLE_BOOKS_API_KEY:
    raise RuntimeError("GOOGLE_BOOKS_API_KEY not found")


def search_google_books(search_term : str):
    """
    Query Google Books and return the top candidate.

    Args:
        search_term: Normalized search string.

    Returns:
        First volume result dict, or None if no results are found.
    """
    params = {
        "q": search_term,
        "maxResults": MAX_RESULTS,
        "key": GOOGLE_BOOKS_API_KEY,
    }

    with httpx.Client(timeout=5.0) as client: # Short timeout to prevent worker blocking on external API
        resp = client.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get("items", [])


    return candidates[0]

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
    authors = v.get("authors", [])
    genres = v.get("categories", [])
    description = v.get("description")

    print(description)

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

def filter_books(candidates : list[dict]) -> dict | None:
    # placeholder for now, will implement logic to filter google_books results to the most relevant candidate
    pass
