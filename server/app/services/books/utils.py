import re
import unicodedata
from typing import List

def normalize_title(title: str) -> str:
    """
    Normalize a book title for identity comparison.

    Example:
    "Harry Potter & the Goblet of Fire!" -> "harry potter and the goblet of fire"
    """
    return normalize_text(title)

def normalize_authors(authors: List[str]) -> List[str]:
    """
    Normalize and sort author names for identity comparison.

    Example:
    ["J. K. Rowling", " Emily  Sanderson! "] -> ["emily sanderson", "jk rowling"]
    """
    normalized = [normalize_text(a) for a in authors if a]
    return sorted(normalized)


def normalize_text(text: str) -> str:
    """
    Base text normalization shared by titles and authors.
    """
    if not text:
        return ""

    text = text.lower()

    # Normalize unicode characters (é -> e, etc.)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    text = text.replace("&", " and ")

    # Remove punctuation / symbols (keep letters and numbers)
    text = re.sub(r"[^\w\s]", " ", text)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()
