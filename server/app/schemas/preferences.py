from pydantic import BaseModel, Field

class PreferencesPost(BaseModel):
    user_id: int
    preferred_genres: list[str] = Field(default_factory=list)
    preferred_authors: list[str] = Field(default_factory=list)
    excluded_books: list[str] = Field(default_factory=list)

class PreferencesCreate(BaseModel):
    user_id: int
    preferred_genres: dict[str,float] = {}
    preferred_authors: dict[str,float] = {}
    excluded_books: list[str] = []
