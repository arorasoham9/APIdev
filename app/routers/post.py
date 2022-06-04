from .. import models, schemas, utils,oath2
from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, UserResponse, Post, PostResponse, PostCreate
from typing import List


router = APIRouter(prefix = '/posts',
                    tags= ['Posts'])


@router.get("/", response_model = List[PostResponse])
def get_Posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts =  db.query(models.Post).all()
    return posts


@router.get("/all", response_model = List[PostResponse])
def getUserPosts(db:Session =Depends(get_db), curuser: User = Depends(oath2.get_User)):
    userposts = db.query(models.Post).filter(models.Post.created_by == curuser.username).all()
    if userposts is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail ="No posts were found.")
    return userposts
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= PostResponse)
def make_Post(post: PostCreate,db: Session = Depends(get_db), curuser: User = Depends(oath2.get_User)):
    # cursor.execute(""" INSERT INTO posts (content,title,published) VALUES (%s, %s, %s) RETURNING *""",(new_post.content, new_post.title, new_post.published))
    # newPost = cursor.fetchone()
    # connection.commit()
    

    post = post.dict()
    post["created_by"] =curuser.username
    newPost = models.Post(**post)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.get("/{id}", response_model = PostResponse)
def getOnePost(id:int,db: Session = Depends(get_db), curuser: User = Depends(oath2.get_User)):
    # cursor.execute("""SELECT * FROM posts  WHERE id = %s""", (str(id))) 
    # newPost = cursor.fetchone()
    # newPost = db.query(models.Post).
    # return {"data": newPost}

    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if posts is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with {id} was not found.")
    return posts
    


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def del_post(id: int,db: Session = Depends(get_db), curuser: User = Depends(oath2.get_User) ):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # delPost = cursor.fetchone()
    # connection.commit()

    del_post = db.query(models.Post).filter(models.Post.id == id).first()
    if del_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with ID {id} was not found.")
    if curuser.username != del_post.create_by:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = f"You do not have permissions to delete this post.")
    del_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


# @app.get("/sqlalchemy/")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}




@router.put("/{id}", response_model = PostResponse)
def updatePost(id:int, post: PostCreate,db: Session = Depends(get_db), curuser: User = Depends(oath2.get_User)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (post.title, post.content, (str(id))))
    # updatedPost = cursor.fetchone()
    update = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = update.first()
    print(type(updatedPost))
    
    if updatedPost is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with ID {id} was not found.")
    if curuser.username != updatedPost.created_by:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = f"You do not have permissions to update this post.")
    update.update(post.dict(), synchronize_session = False)
    db.commit()
    return  update.first()
    # connection.commit()
    # return {"data": updatedPost}
