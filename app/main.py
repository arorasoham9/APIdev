from contextlib import nullcontext
from logging.handlers import MemoryHandler
from multiprocessing import synchronize
from sre_constants import SUCCESS
from turtle import delay
from typing import List
from xml.etree.ElementPath import find
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep

from sqlalchemy import Identity, null
from . import models
from .schemas import Post, PostResponse, User, UserResponse
from .database import engine,get_db

from sqlalchemy.orm import Session




models.Base.metadata.create_all(bind = engine)
app = FastAPI()




while(True):
    try:
        connection = psycopg2.connect(host='localhost', database ='FastAPI', user = 'postgres', password = 'College@1403', cursor_factory= RealDictCursor)
        cursor = connection.cursor()
        print("DB connection was successful")
        break
    except Exception as error:

        print("Connection to DB failed.")
        print("Error: ", error)
        print("Retrying in 5 seconds.")
        sleep(5)
        


       
@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!!!!!! Send Money"}

@app.get("/posts")
def get_Posts(db: Session = Depends(get_db), response_Model = list[PostResponse]):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts =  db.query(models.Post).all()
    return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model= PostResponse)
def make_Post(post: Post,db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (content,title,published) VALUES (%s, %s, %s) RETURNING *""",(new_post.content, new_post.title, new_post.published))
    # newPost = cursor.fetchone()
    # connection.commit()
    
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@app.get("/posts/{id}", response_model = PostResponse)
def getOnePost(id:int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts  WHERE id = %s""", (str(id))) 
    # newPost = cursor.fetchone()
    # newPost = db.query(models.Post).
    # return {"data": newPost}

    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if posts is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with {id} was not found.")
    return posts
    


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def del_post(id: int,db: Session = Depends(get_db) ):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # delPost = cursor.fetchone()
    # connection.commit()
    del_post = db.query(models.Post).filter(models.Post.id == id)
    if del_post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with ID {id} was not found.")
        detail = f"Post with {id} not found"
    del_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


# @app.get("/sqlalchemy/")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}




@app.put("/posts/{id}", response_model = PostResponse)
def updatePost(id:int, post: Post,db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (post.title, post.content, (str(id))))
    # updatedPost = cursor.fetchone()
    update = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = update.first()
    
    if updatedPost is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with ID {id} was not found.")
    update.update(post.dict(), synchronize_session = False)
    db.commit()
    return  update.first()
    # connection.commit()
    # return {"data": updatedPost}

@app.post("/users", status_code= status.HTTP_201_CREATED, response_model = UserResponse)
def createUser(user: User,db: Session = Depends(get_db)):
    sameUsername = db.query(models.User).filter(models.User.username == user.username).first()
    sameEmail = db.query(models.User).filter(models.User.email == user.email).first()
    if sameEmail is not None:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail = f"User with email:'{user.email}' exists.")
    if sameUsername is not None:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail = f"User with username: '{user.username}' exists.")
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser




    

    
    



