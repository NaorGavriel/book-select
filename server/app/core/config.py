import os
from dotenv import load_dotenv

load_dotenv()

# FASTAPI
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

if CORS_ORIGINS:
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS.split(",")]
else:
    CORS_ORIGINS = []

REDIS_JOB_URL = os.getenv("REDIS_JOB_URL")
RATELIMIT_REDIS_URL = os.getenv("RATELIMIT_REDIS_URL")
# OCR api
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google api settings
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
MAX_RESULTS = os.getenv("GOOGLE_BOOKS_MAX_RESULTS")

# Settings : 
BOOK_CACHE_THRESHOLD = float(os.getenv("BOOK_CACHE_THRESHOLD"))

# JWT and Authentication
JWT_SECRET = os.getenv("JWT_SECRET")
HASHING_ALGO = os.getenv("HASHING_ALGORITHM")

TOKEN_EXPIRE_MINUTES = os.getenv("JWT_EXPIRATION_TIME_MINUTES")
if TOKEN_EXPIRE_MINUTES is not None:
    TOKEN_EXPIRE_MINUTES : float = float(TOKEN_EXPIRE_MINUTES)

JWT_EXPIRATION_TIME_REFRESH = os.getenv("JWT_EXPIRATION_TIME_REFRESH")
if JWT_EXPIRATION_TIME_REFRESH is not None:
    JWT_EXPIRATION_TIME_REFRESH : float = float(JWT_EXPIRATION_TIME_REFRESH)

# LOGGING
API_LOGGER_NAME = os.getenv("API_LOGGER_NAME")
