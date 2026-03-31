"""
Unit tests for text normalization utilities.

Covers:
- normalize_text: casing, punctuation, unicode, whitespace
- normalize_title: wrapper around normalize_text
- normalize_authors: normalization + sorting + filtering

These are pure unit tests with no external dependencies.
"""
import pytest
from app.utils.text import (
    normalize_text,
    normalize_title,
    normalize_authors,
)


# =========================
# normalize_text
# =========================

def test_normalize_text_basic():
    assert normalize_text("Hello World") == "hello world"


def test_normalize_text_punctuation_removed():
    assert normalize_text("Hello, World!") == "hello world"


def test_normalize_text_ampersand():
    assert normalize_text("War & Peace") == "war and peace"


def test_normalize_text_unicode():
    """Accented characters should be stripped (é → e)."""
    assert normalize_text("Café") == "cafe"


def test_normalize_text_extra_whitespace():
    assert normalize_text("  hello   world  ") == "hello world"


def test_normalize_text_empty():
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_normalize_text_numbers_preserved():
    assert normalize_text("Book 123!") == "book 123"


# =========================
# normalize_title
# =========================

def test_normalize_title():
    title = "Harry Potter & the Goblet of Fire!"
    expected = "harry potter and the goblet of fire"

    assert normalize_title(title) == expected


def test_normalize_title_empty():
    assert normalize_title("") == ""


# =========================
# normalize_authors
# =========================

def test_normalize_authors_basic():
    authors = ["J. K. Rowling", "Emily Sanderson"]
    result = normalize_authors(authors)

    assert result == ["emily sanderson", "j k rowling"]


def test_normalize_authors_sorting():
    authors = ["b author", "a author"]
    result = normalize_authors(authors)

    assert result == ["a author", "b author"]


def test_normalize_authors_whitespace_and_punctuation():
    authors = ["  J. K. Rowling! ", "Emily   Sanderson  "]
    result = normalize_authors(authors)

    assert result == ["emily sanderson", "j k rowling"]


def test_normalize_authors_ignores_empty():
    authors = ["J. K. Rowling", "", None]
    result = normalize_authors(authors)

    assert result == ["j k rowling"]