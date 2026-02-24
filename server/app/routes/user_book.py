from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.services.user_book import add_user_book
from app.db import get_db
from app.schemas.user_book import UserBookCreateSchema

router = APIRouter(prefix='/user_books')

@router.post("/")
async def post_user_book(user_book_data : UserBookCreateSchema, user_id: int = 1, db: Session = Depends(get_db)):
    try:
        title = user_book_data.title
        author = user_book_data.author
        result = add_user_book(db=db, title=title, author=author, user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
            )