from contextlib import nullcontext
from logging.handlers import MemoryHandler
from multiprocessing import synchronize
from pyexpat import model
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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import utils
from . import models
from .schemas import Post, PostResponse, User, UserResponse
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
from . import schemas, utils




models.Base.metadata.create_all(bind = engine)
app = FastAPI()



origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# while(True):
#     try:
#         connection = psycopg2.connect(host='localhost', database ='FastAPI', user = 'postgres', password = 'College@1403', cursor_factory= RealDictCursor)
#         cursor = connection.cursor()
#         print("DB connection was successful")
#         break
#     except Exception as error:

#         print("Connection to DB failed.")
#         print("Error: ", error)
#         print("Retrying in 5 seconds.")
#         sleep(5)
        

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
       
@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!!!!!! Send Money"}
      





    

    
    



