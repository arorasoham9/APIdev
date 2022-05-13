from contextlib import nullcontext
from xml.etree.ElementPath import find
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

my_posts = [{"title":"My name", "content": "james carter","id": 2},
            {"title":"My death", "content": "in 1947","id": 3}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int



def findPost(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None
    
        
        
@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!!!!!!"}

@app.get("/posts")
def get_Posts():
    cursor.execute()
    return {"data": my_posts}

@app.post("/posts")
def make_Post(new_post: Post, status_code = status.HTTP_201_CREATED):
    postdict = new_post.dict()
    id = randrange(0, pow(10, 10))
    while findPostID(id) is not None:
        id = randrange(0, pow(10, 10))
    postdict['id'] = id
    my_posts.append(postdict)
    return {"post_detail": my_posts}



@app.get("/posts/{id}")
def getOnePost(id:int):
    p = findPost(id)
    if p is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with {id} was not found.")
    return {"details": p}
    


def findPostID(id):
    for i, p in enumerate(my_posts):
        if(p['id'] == id):
            return i
    return None

@app.delete("/posts/{id}")
def del_post(id: int, status_code = status.HTTP_204_NO_CONTENT ):
    index = findPostID(int(id))
    if not index:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with ID {id} was not found.")
        detail = f"Post with {id} not found"
    my_posts.pop(index)
    return {"message": "The post was successfully deleted.",
            "details": my_posts}


@app.put("/posts/{id}")
def updatePost(id:int, post: Post):
    id = findPostID(id)
    print(post)
    postDict = post.dict()
    if id is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with ID {id} was not found.")
    if findPostID(postDict['id']) is not None:
        raise HTTPException(status_code =  status.HTTP_409_CONFLICT, 
                            detail ="post with same ID found in pool")
    my_posts[id] = postDict
    return {"data": my_posts}
    
    



