from fastapi import Depends,APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..utils import hash_password

router = APIRouter(
    tags=['Users']
)

@router.post('/users', status_code=201)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    #hash password
    user.password = hash_password(user.password)
    #create new user
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users', status_code=200)
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/users/{id}')
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id was {id} not found")
    return user