"""
Google Books integration.

Handles external search requests and transforms API responses
into the internal book data format.
"""
import httpx
from app.core.config import GOOGLE_BOOKS_API_KEY, MAX_RESULTS
from app.utils.text import normalize_authors, normalize_title, normalize_text
MAX_DESCRIPTION_LENGTH = 1000
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

if not GOOGLE_BOOKS_API_KEY:
    raise RuntimeError("GOOGLE_BOOKS_API_KEY not found")


def search_google_books(search_term : str = None, title : str = None, author : str = None):

    """
    Query Google Books and return the top candidate.

    Args:
        search_term: Normalized search string.
        title: normalized book title.
        author : normalized book author.

    Returns:
        First volume result dict, or None if no results are found.
    """
    if (title and author): # searching by title and author if exists or by a search term
        query_term = f'intitle:"{title}" inauthor:"{author}"'
    else :
        query_term = search_term

    if query_term is None:
        return None

    params = {
        "q": query_term,
        "langRestrict": "en",
        "maxResults": MAX_RESULTS,
        "key": GOOGLE_BOOKS_API_KEY,
    }

    with httpx.Client(timeout=5.0) as client: # Short timeout to prevent worker blocking on external API
        resp = client.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get("items", [])
        best_book = filter_results(items=candidates, author=author)

    return best_book

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
    authors = v.get("authors")
    description = v.get("description")
    genres = v.get("categories", [])

    if len(description) > MAX_DESCRIPTION_LENGTH: # truncating long descriptions
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

    if not filtered:
        return None

    return filtered[0] # most relevant
