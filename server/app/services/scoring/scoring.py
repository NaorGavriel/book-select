from app.models.book import Book
from app.dto.book_result import BookResult
from app.models.user_book import UserBook
from app.models.enums import Decision
from sqlalchemy.orm import Session
from sqlalchemy import select, literal


def score_book(candidate: Book, user_id: int, similarity : float, similar_book : Book) -> BookResult:
    """
    Generate a BookResult decision based on similarity score.

    Applies threshold-based logic to classify a candidate book
    as strong_match, consider, or avoid, and provides a short
    human-readable explanation.

    Args:
        candidate (Book): The book being evaluated.
        user_id (int): ID of the user for whom scoring is performed.
        similarity (float): Cosine similarity score (0.0-1.0).
        similar_book (Book | None): Most similar previously-read book.

    Returns:
        BookResult: Structured scoring result.
    """
    if similar_book is None:
        decision = Decision.avoid
        reasoning = "No similar books found in your reading history."
    elif similarity >= 0.5:
        decision = Decision.strong_match
        reasoning = (
            f"Very similar to '{similar_book.title}' "
            f"by {similar_book.authors[0]}."
        )
    elif similarity >= 0.3:
        decision = Decision.consider
        reasoning = (
            f"Moderately similar to '{similar_book.title}' "
            f"by {similar_book.authors[0]}."
        )
    else :
        decision = Decision.avoid
        reasoning = "No similar books found in your reading history."

    book_result = BookResult(
            user_id=user_id,
            authors=candidate.authors,
            title=candidate.title,
            confidence=round(similarity, 3),
            decision=decision,
            explanation=reasoning
        )
    
    return book_result

def get_best_similarity(db: Session, candidate: Book, user_id: int) -> tuple[Book | None, float]:
    """
    Retrieve the user's most similar previously-read book.

    Uses pgvector cosine distance to compute similarity
    between the candidate embedding and the user's read books.
    Excludes the candidate itself.

    Args:
        db (Session): Active database session.
        candidate (Book): Book to compare against user history.
        user_id (int): User identifier.

    Returns:
        tuple[Book | None, float]:
            - Most similar Book (or None if not found)
            - Cosine similarity score (0.0 if none)
    """

    if candidate.embedding is None:
        return None, 0.0
    
    cand_embed = list(candidate.embedding) 
    distance_expr = Book.embedding.op("<=>")(cand_embed)

    
    similarity_expr = literal(1.0) - distance_expr # convert cosine distance to cosine similarity

    stmt = (
        select(
            Book,
            similarity_expr.label("similarity")
        )
        .join(UserBook, UserBook.book_id == Book.id)
        .where(UserBook.user_id == user_id)
        .where(Book.embedding.isnot(None))
        .where(Book.id != candidate.id)  # exclude same book
        .order_by(distance_expr)  # smaller distance = more similar
        .limit(1)
    )

    result = db.execute(stmt).first()

    if result is None:
        return None, 0.0

    book, similarity = result
    return book, float(similarity)