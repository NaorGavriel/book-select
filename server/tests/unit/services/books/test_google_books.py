"""
Unit tests for google_books module.

Covers:
- query construction
- result filtering
- data extraction
- API integration (mocked)
"""
import pytest
from app.services.books.google_books import (
    _build_query,
    filter_results,
    extract_book_data,
    search_google_books,
)

@pytest.fixture
def valid_item():
    """Returns a valid Google Books API item."""
    return {
        "volumeInfo": {
            "title": "Test Book",
            "authors": ["John Doe"],
            "description": "A good book",
            "categories": ["Fiction"],
            "language": "en",
        }
    }

@pytest.mark.parametrize(
    "search_term, title, author, expected",
    [
        ("harry potter", None, None, "harry potter"),
        (None, "Harry Potter", "Rowling", 'intitle:"Harry Potter" inauthor:"Rowling"'),
        (None, None, None, None),
    ],
)
def test_build_query(search_term, title, author, expected):
    """Builds correct query string based on inputs."""
    assert _build_query(search_term, title, author) == expected

def test_filter_results_valid(valid_item):
    """Returns first valid English item."""
    items = [
        {"volumeInfo": {"language": "fr"}},  # invalid
        valid_item,
    ]

    result = filter_results(items)

    assert result == valid_item

def test_filter_results_no_valid():
    """Returns None when no valid items exist."""
    items = [
        {"volumeInfo": {"language": "fr"}},
    ]

    assert filter_results(items) is None

def test_filter_results_author_match(valid_item):
    """Filters results by matching author."""
    result = filter_results([valid_item], author="john doe")

    assert result == valid_item

def test_filter_results_author_mismatch(valid_item):
    """Returns None when author does not match."""
    result = filter_results([valid_item], author="someone else")

    assert result is None

def test_extract_book_data_basic(valid_item):
    """Extracts core fields correctly."""
    result = extract_book_data(valid_item)

    assert result["title"] == "Test Book"
    assert result["authors"] == ["John Doe"]
    assert result["genres"] == ["Fiction"]
    assert result["source"] == "google_books"

def test_extract_book_data_isbn():
    """Extracts ISBN_13 when present."""
    item = {
        "volumeInfo": {
            "industryIdentifiers": [
                {"type": "ISBN_13", "identifier": "123"}
            ]
        }
    }

    result = extract_book_data(item)

    assert result["isbn_13"] == "123"

def test_extract_book_data_truncates_description():
    """Truncates description to max length."""
    long_desc = "a" * 2000

    item = {
        "volumeInfo": {
            "title": "Book",
            "authors": ["Author"],
            "description": long_desc,
        }
    }

    result = extract_book_data(item)

    assert len(result["description"]) == 1000

def test_extract_book_data_no_description():
    """Handles missing description without crashing."""
    item = {
        "volumeInfo": {
            "title": "Book",
            "authors": ["Author"],
            "description": None,
        }
    }

    result = extract_book_data(item)

    assert result["description"] is None

def test_search_google_books_success(mocker, valid_item):
    """Returns filtered result from fetched items."""
    mocker.patch(
        "app.services.books.google_books._fetch_books",
        return_value=[valid_item],
    )

    result = search_google_books(search_term="test")

    assert result == valid_item

def test_search_google_books_no_query():
    """Returns None when no query can be built."""
    result = search_google_books()

    assert result is None