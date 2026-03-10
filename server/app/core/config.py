import os
from dotenv import load_dotenv

load_dotenv()

class AuthConfig:
    JWT_SECRET = os.getenv("JWT_SECRET")
    HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
    ACCESS_TOKEN_EXP_MINUTES = float(os.getenv("JWT_EXPIRATION_TIME_MINUTES", 7))
    REFRESH_TOKEN_EXP_DAYS = float(os.getenv("JWT_EXPIRATION_TIME_REFRESH", 30))
    

class GeneralConfig:
    MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE"))

    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")
    REDIS_JOB_URL = os.getenv("REDIS_JOB_URL", "redis://redis:6379/0")
    REDIS_RATELIMIT_URL = os.getenv("RATELIMIT_REDIS_URL", "redis://redis:6379/1")

    if CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",")]
    else:
        CORS_ALLOWED_ORIGINS = []

    BOOK_CACHE_THRESHOLD = float(os.getenv("BOOK_CACHE_THRESHOLD",0.8))
    API_LOGGER_NAME = os.getenv("API_LOGGER_NAME", "default_logger")
    STORAGE_BACKEND= os.getenv("STORAGE_BACKEND", "local")

class AWSConfig:
    AWS_REGION = os.getenv("AWS_REGION")
    BUCKET_NAME = os.getenv("BUCKET_NAME")

class APIsConfig:
    # Google api settings
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
    MAX_RESULTS = int(os.getenv("GOOGLE_BOOKS_MAX_RESULTS", 5))

    # OpenAi api settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
