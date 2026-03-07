from sqlalchemy.orm import Session
from app.models.user import User



def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by email address.

    Args:
        db (Session): Active database session.
        email (str): User's email address.

    Returns:
        User | None: Matching user if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user by id.

    Args:
        db (Session): Active database session.
        user_id (int): User's id.

    Returns:
        User | None: Matching user if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, hashed_password: str) -> User:
    """
    Create and persist a new user.

    Args:
        db (Session): Active database session.
        email (str): User's email address.
        hashed_password (str): hashed password.

    Returns:
        User: The newly created and persisted user entity.
    """
    user = User(
        email=email,
        password_hash=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
