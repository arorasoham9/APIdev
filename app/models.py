from email.policy import default
from ssl import create_default_context
from tkinter import CASCADE
from .database import Base
from sqlalchemy import Column,ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
  
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content =  Column(String, nullable = False)
    published = Column(Boolean, server_default= 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = text('now()'))
    created_by = Column(String, ForeignKey("users.username", ondelete= CASCADE), nullable = False )
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    username = Column(String, nullable = False, primary_key = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False, unique = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = text('now()'))




