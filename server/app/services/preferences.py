from app.crud.preferences import create_preferences, get_preferences_by_user_id, update_preferences
from app.schemas.preferences import PreferencesPost, PreferencesCreate
from app.models.preferences import Preferences
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class InvalidUserId(Exception):
    """
    Raised when a preferences operation references a user that does not exist in the system.
    """
    pass

def create_user_preferences(preferences : PreferencesPost, db: Session):
    """
    Create a new preferences record for a user.

    - receives raw user intent (lists of genres/authors)
    - assigns placeholder scores (domain logic will evolve later)
    - delegates persistence to the CRUD layer

    Args:
        preferences: Raw preferences sent by the client.
        db: SQLAlchemy session.

    Returns:
        The newly created Preferences ORM object.

    Raises:
        InvalidUserId: If the referenced user does not exist.
    """

    preferred_genres = {genre: 0.5 for genre in preferences.preferred_genres} # placeholder values
    preferred_authors = {author: 0.5 for author in preferences.preferred_authors} # placeholder values

    user_pref = PreferencesCreate(
        user_id=preferences.user_id,
        preferred_genres=preferred_genres,
        preferred_authors=preferred_authors,
        excluded_books=preferences.excluded_books
    )
    try:
        return create_preferences(db,user_pref)
    except IntegrityError as e:
        db.rollback()
        raise InvalidUserId("Invalid user ID")  

def update_user_preferences(new_preferences : PreferencesPost, db: Session):
    """
    Update an existing user's preferences by merging new input with previously stored preferences.

    Update semantics:
    - New genres/authors are merged with existing ones.
    - Excluded books are merged.

    Args:
        new_preferences: New preference signals from the client.
        db: SQLAlchemy session (request-scoped).

    Returns:
        The updated Preferences ORM object.

    Raises:
        InvalidUserId: If the user has no existing preferences.
    """
    existing = get_preferences_by_user_id(db, new_preferences.user_id)

    if existing is None:
        raise InvalidUserId("UpdateUserPreferences : User not found")
    
    combined_genres = expand_scores(existing.genres)
    combined_authors = expand_scores(existing.authors)

    combined_genres.extend(new_preferences.preferred_genres)
    combined_authors.extend(new_preferences.preferred_authors)

    combined_excluded = list(set(existing.excluded_books + new_preferences.excluded_books))

    combined_preferences = PreferencesPost(
        user_id=new_preferences.user_id,
        preferred_genres=combined_genres,
        preferred_authors=combined_authors,
        excluded_books=combined_excluded,
    )

    genre_scores, author_scores = calculate_scores(combined_preferences)

    # updating existing preferences with new genres, authors, books and scores
    existing.genres = genre_scores
    existing.authors = author_scores
    existing.excluded_books = combined_excluded
    res = update_preferences(db, existing)

    return res

def calculate_scores(preferences: PreferencesPost):
    # placeholder values
    genre_scores = {genre: 0.5 for genre in preferences.preferred_genres}
    author_scores = {author: 0.5 for author in preferences.preferred_authors}

    return genre_scores, author_scores

def expand_scores(scores: dict[str, float]) -> list[str]:
    return list(scores.keys())



