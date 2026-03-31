"""
Unit tests for the score_book function.

Verifies that similarity thresholds correctly map to decisions
(strong_match, consider, avoid) based on user reading history.
"""
import pytest
from app.services.scoring.scoring import score_book
from app.models.enums import Decision


class DummyBook:
    def __init__(self, title, authors):
        self.title = title
        self.authors = authors


@pytest.mark.parametrize(
    "similarity, has_similar, expected_decision",
    [
        (0.7, True, Decision.strong_match),
        (0.4, True, Decision.consider),
        (0.1, True, Decision.avoid),
    ],
)
def test_score_book_decision(similarity, has_similar, expected_decision):
    """Assigns correct decision based on similarity thresholds."""
    candidate = DummyBook("Candidate", ["Author"])
    similar = DummyBook("Book", ["Author"]) if has_similar else None

    result = score_book(candidate, 1, similarity, similar)

    assert result.decision == expected_decision