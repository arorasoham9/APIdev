import email
from fastapi import HTTPException, status
from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
oath2_scheme = OAuth2PasswordBearer(tokenUrl= 'login/')
ALGORITHM = "HS256"
EXPIRATION_TIME =  30
SECRET_KEY ="jamescarterisdeaddeadisjamescartermynameisanthonygonsalvesIameebuhatela"

def create_token(payload: dict):
    payloadcpy = payload.copy()
    expire = datetime.now()+ timedelta(minutes= EXPIRATION_TIME) 
    payloadcpy.update({"exp": expire})
    encoded_jwt = jwt.encode(payloadcpy,SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM )
    
        email : EmailStr = payload.get("email")

        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

def get_User(token: str = Depends(oath2_scheme)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail= f"Could not validate credentials",
                           headers = {"WWW-Authenticate": "Bearer"})
    return verify_token(token, credential_exception)