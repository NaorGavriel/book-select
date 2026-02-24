from app.models.book import Book
from app.dto.book_result import BookResult
from app.models.user_book import UserBook
from app.models.enums import Decision
from sqlalchemy.orm import Session
from sqlalchemy import select, literal


def score_book(candidate: Book, user_id: int, similarity : float, similar_book : Book) -> BookResult:

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
    Returns the most similar previously-read book for the user,
    excluding the same book_id as the candidate.
    """

    if candidate.embedding is None:
        return None, 0.0
    

    cand_embed = list(candidate.embedding)
    distance_expr = Book.embedding.op("<=>")(cand_embed)

    # convert cosine distance to cosine similarity
    similarity_expr = literal(1.0) - distance_expr

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