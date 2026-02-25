from app.services import auth
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.user import User 

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user credentials and issue a JWT access token.

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
    
    token = auth.create_token(data={"sub": user.email}) # Create JWT token with email as subject

    return {"access_token": token, "token_type": "bearer"}