from asyncio import streams
from tokenize import String
from turtle import st
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
    

class UserResponse(BaseModel):
    created_at: datetime
    username: str
    email: EmailStr


    class Config:
        orm_mode = True

class User_Login(BaseModel):
    email: EmailStr
    password: str

class Authenticated(BaseModel):
    email: EmailStr
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
