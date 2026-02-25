from sqlalchemy.orm import Session
from app.crud.users import get_user_by_email

class UserNotFound(Exception):
    pass

def get_user(db : Session, email: str):
    """
    Retrieve a user by email or raise an exception if not found.

    Args:
        db (Session): Active database session.
        email (str): User email address.

    Returns:
        User: User object.

    Raises:
        UserNotFound: If no user exists with the given email.
    """
    user = get_user_by_email(db, email)

    if user is None:
        raise UserNotFound(f"No user found for {email}")

    return user