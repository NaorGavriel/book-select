from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.crud.users import get_user_by_email, create_user
from app.db import get_db

router = APIRouter(prefix='/users')


@router.post("/", response_model=UserRead)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = create_user(
        db,
        email=user_in.email,
        password=user_in.password
    )

    return user
