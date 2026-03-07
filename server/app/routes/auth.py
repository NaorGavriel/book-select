from app.services import auth
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import refresh_access_token, InvalidRefreshToken
from app.core.limiter import limiter


router = APIRouter()

@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
    
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age= 30 * 24 * 60 * 60,       
    )


    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
@limiter.limit("5/minute")
def logout(request: Request, response: Response):
    response.delete_cookie("refresh_token")

@router.post("/refresh")
@limiter.limit("5/minute")
def refresh(request: Request, refresh_token: str = Cookie(None)):
    try:
        new_access_token = refresh_access_token(refresh_token)
    except InvalidRefreshToken as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    return {"access_token": new_access_token}