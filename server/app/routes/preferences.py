from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from app.schemas.preferences import PreferencesPost
from app.services.preferences import create_user_preferences, update_user_preferences, InvalidUserId
from app.db import get_db
from app.core.limiter import limiter

router = APIRouter(prefix='/preferences')

@router.post("/")
@limiter.limit("5/minute")
async def post_preferences(request : Request, preferences : PreferencesPost, db: Session = Depends(get_db)):
    try:
        result = create_user_preferences(preferences, db)
        return result
    except InvalidUserId as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
            )

@router.patch("/")
@limiter.limit("5/minute")
async def update_preferences(request : Request, new_preferences : PreferencesPost, db: Session = Depends(get_db)):
    try:
        result = update_user_preferences(new_preferences, db)
        return result
    except InvalidUserId as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
            )
    