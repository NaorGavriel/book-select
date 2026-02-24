from pydantic import BaseModel

class UserBookCreateSchema(BaseModel):
    title: str
    author: str

    class Config:
        from_attributes = True

