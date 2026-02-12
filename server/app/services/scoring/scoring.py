from app.models.book import Book
from app.dto.book_result import BookResult
from app.models.enums import Decision
def score_books(books: list[Book], user_id: int) -> list[BookResult]:
    results = []
    for book in books:
        book_result = BookResult(
            user_id=user_id,
            authors=book.authors,
            title=book.title,
            confidence=1.0, # placeholder for testing
            decision= Decision.strong_match,
            explanation="Good"
        )

        results.append(book_result)
    
    
    return results
