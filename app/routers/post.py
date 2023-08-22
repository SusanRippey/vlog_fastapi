from fastapi import Depends,APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from . import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    tags=['Posts']
)



@router.get('/')
def home(current_user: dict =  Depends(oauth2.get_current_user)):

    return {'Welcome': current_user.email, 'user_id': current_user.id}

@router.get('/posts', response_model=list[schemas.Post])
def get_posts(
    db:Session = Depends(get_db),
    current_user: dict =  Depends(oauth2.get_current_user),
    limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.like(f"%{search}%")).limit(limit).offset(skip).all()
    return posts





@router.post('/posts', status_code=201)
def create_post(post: schemas.CreatePost, db:Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Created post successfully", "post": new_post}


@router.get('/posts/{id}')
def get_post(id: int, db:Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id was {id} not found")
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")
    return {post}


@router.delete('/posts/{id}')
def delete_post(id: int, db:Session= Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id).first()    
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id was {id} not found")
    if delete_post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")
    
    db.delete(delete_post)
    db.commit()
    return {"message": f"Post with id {id} has been deleted successfully", "deleted_post": delete_post}


@router.put('/posts/{id}')
def update_post(id: int, updated_post: schemas.BasePost, db: Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    if post_query.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")
    post_query.update(updated_post.model_dump())
    db.commit()
    return {"message": "Post updated successfully", "updated_post": post_query.first()}