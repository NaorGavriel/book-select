from sqlalchemy.orm import Session
from app.crud.users import get_user_by_email, get_user_by_id

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

def get_user_by_user_id(db : Session, user_id: int):
    """
    Retrieve a user by id or raise an exception if not found.

    Args:
        db (Session): Active database session.
        user_id (str): User id.

    Returns:
        User: User object.

    Raises:
        UserNotFound: If no user exists with the given id.
    """
    user = get_user_by_id(db, user_id)

    if user is None:
        raise UserNotFound(f"User {user_id} Not Found.")

    return user