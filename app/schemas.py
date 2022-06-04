from asyncio import streams
from tokenize import String
from pydantic import BaseModel,  EmailStr
from datetime import datetime



    
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostCreate):
    
    created_by: str

class User_Login(BaseModel):
    email: EmailStr
    password: str


class User_return(BaseModel):
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class PostResponse(Post):
    id: int
    created_at: datetime
    created_by: str
    owner: User_return
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    


class Authenticated(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    created_at: datetime
    username: str
    email: EmailStr


    class Config:
        orm_mode = True

    

