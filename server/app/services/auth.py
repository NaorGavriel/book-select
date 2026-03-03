from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import bcrypt
from app.services.users import get_user, UserNotFound
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.crud.users import create_user
from app.core.config import AuthConfig

class InvalidRefreshToken(Exception):
    pass

if not AuthConfig.JWT_SECRET:
    raise RuntimeError("Missing JWT_SECRET_KEY")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/token/")


def authenticate_user(db : Session, email: str, password: str) -> User | None:
    """
    Authenticate user credentials.

    Args:
        db (Session): Active database session.
        email (str): User email.
        password (str): Plain-text password.

    Returns:
        User | None: Authenticated user or None if invalid.
    """
    user = get_user(db, email)

    if not user:
        return False
    
    if not verify_password(password=password, hashed_password=user.password_hash):
        return False
    
    return user


def create_access_token(data: dict):
    """
    Generate a signed JWT access token.

    Args:
        data (dict): Payload to encode.

    Returns:
        str: Encoded JWT.
    """
    data_to_encode = data.copy()

    expires_delta = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXP_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    data_to_encode.update({"exp":expire,
                           "type": "access"})

    encoded_jwt = jwt.encode(data_to_encode, AuthConfig.JWT_SECRET, algorithm=AuthConfig.HASH_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Generate a signed JWT refresh token.

    Args:
        data (dict): Payload to encode.

    Returns:
        str: Encoded JWT.
    """
    data_to_encode = data.copy()

    expires_delta = timedelta(days=AuthConfig.REFRESH_TOKEN_EXP_DAYS)
    expire = datetime.now(timezone.utc) + expires_delta
    data_to_encode.update({"exp":expire,
                           "type": "refresh"})

    encoded_jwt = jwt.encode(data_to_encode, AuthConfig.JWT_SECRET, algorithm=AuthConfig.HASH_ALGORITHM)
    return encoded_jwt    

# the get_current_user method gets a token as parameter and checks if it can decode into the username, meaning if its a valid token
def get_current_user(token : str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    """
    Validate JWT and return the authenticated user.

    Raises:
        HTTPException: 401 if token is invalid or user not found.
    """
    cred_excep = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't verify user credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decode and validate token
        payload = jwt.decode(token, AuthConfig.JWT_SECRET, algorithms=[AuthConfig.HASH_ALGORITHM])
        email: str = payload.get("sub")
        token_type : str = payload.get("type")
        if email == None or token_type != "access":
            raise cred_excep
    except JWTError:
        raise cred_excep

    try:
        user = get_user(db=db, email=email)
    except UserNotFound:
        raise cred_excep
    
    return user

def refresh_access_token(refresh_token: str) -> str:
    if not refresh_token:
        raise InvalidRefreshToken("Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, AuthConfig.JWT_SECRET, algorithms=[AuthConfig.HASH_ALGORITHM])
    except JWTError:
        raise InvalidRefreshToken("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise InvalidRefreshToken("Invalid token type")

    email = payload.get("sub")
    if not email:
        raise InvalidRefreshToken("Invalid token payload")

    return create_access_token({"sub": email})

def decode_token(token : str):
    try:
        payload = jwt.decode(token, AuthConfig.JWT_SECRET, algorithms=[AuthConfig.HASH_ALGORITHM])
        return payload
    except JWTError:
        return None

def create_new_user(db : Session, email : str, password : str):
    """
    Create a new user with hashed password.

    Args:
        db (Session): Active database session.
        email (str): User email.
        password (str): Plain-text password.

    Returns:
        User: created User object
    """
    user = create_user(db=db, email=email, hashed_password=hash_password(password))
    return user

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Compare plain-text password against bcrypt hash.

    Returns:
        bool: True if password matches, otherwise False.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Returns:
        str: UTF-8 encoded bcrypt hash.
    """
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed_pw