from pydoc import plain
from passlib.context import CryptContext



pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = 'auto')


def Hash(password: str):
    return pwd_context.hash(password)

def verifyPassword(input_password, hashed_password):
    return pwd_context.verify(input_password, hashed_password) 