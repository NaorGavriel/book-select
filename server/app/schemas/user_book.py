from pydantic import BaseModel

class UserBookCreateSchema(BaseModel):
    title: str
    author: str

    class Config:
        from_attributes = True


class UserBookResponse(BaseModel):
    title : str
    authors : list[str]
    description : str
    genres : list[str]

    model_config = {
        "from_attributes": True
    }
