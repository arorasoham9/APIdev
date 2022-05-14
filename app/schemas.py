from tokenize import String
from pydantic import BaseModel,  EmailStr
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(Post): 
    pass


class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    

class UserResponse(User):
    created_at: datetime


    class Config:
        orm_mode = True
