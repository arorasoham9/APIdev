
from .. import models, schemas, utils, oath2
from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, UserResponse, Post, PostResponse, Authenticated, User_Login
from typing import List

router = APIRouter(prefix = '/auth',
                    tags= ['Authentication'])



@router.get("/", response_model = Authenticated)
def authenticate(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Wrong Credentials")
    if not utils.verifyPassword(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Wrong Credentials")
        
    access_token = oath2.create_token(payload =  {"user_email": user_credentials.username})
    return {"access_token": access_token, "token_type":"bearer"}







