from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):

    PG_USER: str
    PG_PW: str
    PG_DB: str
    PG_HOST: str = "db"
    PG_PORT: int = 5432

    REDIS_JOBS_URL: str
    REDIS_RATELIMIT_URL: str

    GOOGLE_BOOKS_API_KEY: str
    GOOGLE_BOOKS_MAX_RESULTS: int = 5

    BOOK_CACHE_THRESHOLD: float = 0.8

    OPENAI_API_KEY: str

    JWT_SECRET: str
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXP_MINUTES: float = 7
    REFRESH_TOKEN_EXP_DAYS: float = 30

    CORS_ALLOWED_ORIGINS: List[str] = []

    API_LOGGER_NAME: str = "default_logger"

    STORAGE_BACKEND: str = "local"

    MAX_IMAGE_SIZE: int

    BUCKET_REGION: str | None = None
    BUCKET_NAME: str | None = None

    DEPLOYMENT_TYPE: str = "local"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.PG_USER}:{self.PG_PW}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )