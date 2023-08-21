from pydantic import BaseModel,EmailStr, Field
from typing import Optional
from datetime import datetime


# Schema for  User
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_no: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True


# Schemas for post
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True
    

class CreatePost(BasePost):
    pass

    
class Post(BasePost):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True


# Schema for Login

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for Token

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

# Schema for vote

class Vote(BaseModel):
    post_id: int
    vote_dir: int = Field(..., description="only accept 0 or 1", ge=0, le=1)