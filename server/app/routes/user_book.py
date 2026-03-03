from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.services.user_book import add_user_book, get_books_of_user
from app.db import get_db
from app.schemas.user_book import UserBookCreateSchema, UserBookResponse
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix='/user_books')

@router.post("/")
async def post_user_book(user_book_data : UserBookCreateSchema, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
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
async def get_user_books(db: Session = Depends(get_db), user : User = Depends(get_current_user)):
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