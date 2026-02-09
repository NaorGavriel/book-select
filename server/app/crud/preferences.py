from sqlalchemy.orm import Session
from app.models.preferences import Preferences
from app.schemas.preferences import PreferencesCreate
from app.db import get_db

def get_preferences_by_user_id(db: Session, user_id: int) -> Preferences | None:
    return db.query(Preferences).filter(Preferences.user_id == user_id).first()


def create_preferences(db: Session, pref : PreferencesCreate) -> Preferences:
    preferences = Preferences(
        user_id=pref.user_id,
        genres=pref.preferred_genres,
        authors=pref.preferred_authors,
        excluded_books=pref.excluded_books
    )

    db.add(preferences)
    db.commit()
    db.refresh(preferences)
    return preferences
