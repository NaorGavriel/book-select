from app.services import auth
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import refresh_access_token, InvalidRefreshToken

router = APIRouter()

@router.post("/token", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user credentials and issue JWT access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): Login form payload.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: 401 if authentication fails.
    """
    user = auth.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age= 30 * 24 * 60 * 60,       
    )


    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh(refresh_token: str = Cookie(None)):
    try:
        new_access_token = refresh_access_token(refresh_token)
    except InvalidRefreshToken as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    return {"access_token": new_access_token}