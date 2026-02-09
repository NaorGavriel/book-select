from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas.preferences import PreferencesPost
from app.services.preferences import create_user_preferences, InvalidUserId
from app.db import get_db

router = APIRouter(prefix='/preferences')

@router.post("/")
async def post_preferences(preferences : PreferencesPost, db: Session = Depends(get_db),):
    try:
        result = create_user_preferences(preferences, db)
        return result
    except InvalidUserId as e:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
    