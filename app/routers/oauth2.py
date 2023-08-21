from jose import jwt,JWTError
from datetime import datetime,timedelta
from .. import schemas,database, models
from sqlalchemy.orm import Session
from fastapi import status,HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from ..confgi import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login') # login is the url where user need to go and validate themself

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minute

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_excpetion):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_excpetion
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_excpetion
    return token_data    

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):

    credentails_excpetion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers= {"WWW-Authenticate":"Bearer"})
    
    user_token = verify_access_token(token, credentails_excpetion) # returns token data 
    current_user = db .query(models.User).filter(models.User.id == user_token.id).first()

    return current_user

    



