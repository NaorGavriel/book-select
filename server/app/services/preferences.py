from app.crud.preferences import create_preferences
from app.schemas.preferences import PreferencesPost, PreferencesCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class InvalidUserId(Exception):
    pass

def create_user_preferences(preferences : PreferencesPost, db: Session):
    

    preferred_genres = {}
    preferred_authors = {}

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
