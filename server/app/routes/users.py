from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserRead
from app.services.auth import create_new_user
from app.db import get_db

router = APIRouter(prefix='/users')

@router.post("/", response_model=UserRead)
def register_user(user_register_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_register_data (UserCreate): Incoming user registration payload.

    Returns:
        UserRead: Newly created user.

    Raises:
        HTTPException: 400 if email already exists.
    """

    try:
        user = create_new_user(
            db=db,
            email=user_register_data.email,
            password=user_register_data.password
        )
        return user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
