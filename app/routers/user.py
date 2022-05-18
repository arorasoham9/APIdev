from .. import models, schemas, utils
from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, UserResponse, Post, PostResponse
from typing import List

router = APIRouter(prefix = '/users',
                    tags = ['Users'])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = UserResponse)
def createUser(user: User,db: Session = Depends(get_db)):
    sameUsername = db.query(models.User).filter(models.User.username == user.username).first()
    sameEmail = db.query(models.User).filter(models.User.email == user.email).first()
    if sameEmail is not None:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail = f"User with email:'{user.email}' exists.")
    if sameUsername is not None:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail = f"User with username: '{user.username}' exists.")
    
    user.password = utils.Hash(user.password)
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.get("/", response_model = List[UserResponse])
def getUsers(db: Session = Depends(get_db)):
    allUsers = db.query(models.User).all()
    return allUsers

@router.get("/{username}", response_model = UserResponse)
def getUsers( username: str, db: Session = Depends(get_db), response_Model = UserResponse):
    oneUser = db.query(models.User).filter(models.User.username == username).first()
    if oneUser is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with username: '{username}' was not found.")
    return oneUser
    

@router.delete("/{username}", status_code = status.HTTP_204_NO_CONTENT)
def deleteUser(username: str, db: Session = Depends(get_db)):
    oneUser = db.query(models.User).filter(models.User.username == username)

    if oneUser is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with username: '{username}' was not found.")
    oneUser.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/{username}")
def changePassword(user: User, username: str, db: Session = Depends(get_db)):
    update = db.query(models.User).filter(models.User.username == username)
    updatedPost = update.first()
    
    if updatedPost is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"User with username: '{username}' was not found.")
     
    update.update(user.dict(), synchronize_session = False)
    db.commit()
    return  update.first()


