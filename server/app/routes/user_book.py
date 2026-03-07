from fastapi import HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from app.services.user_book import add_user_book, get_books_of_user
from app.db import get_db
from app.schemas.user_book import UserBookCreateSchema, UserBookResponse
from app.models.user import User
from app.services.auth import get_current_user
from app.core.rate_limit.limiter import limiter


router = APIRouter(prefix='/user_books')

@router.post("/")
@limiter.limit("50/day")
async def post_user_book(request : Request, user_book_data : UserBookCreateSchema, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    try:
        title = user_book_data.title
        author = user_book_data.author
        result = add_user_book(db=db, title=title, author=author, user_id=user.id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
            )
    

@router.get("/", response_model=list[UserBookResponse])
@limiter.limit("20/minute")
async def get_user_books(request : Request, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
    try:
        books = get_books_of_user(db=db, user_id=user.id)
        if books == []:
            raise HTTPException(
                status_code=404,
                detail=str(e)
                )    
            
        return books
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
            )