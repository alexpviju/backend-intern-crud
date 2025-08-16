from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database,schemas
from ..auth import get_current_user
from typing import List
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/likes", tags=["Likes"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{post_id}")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not db.query(models.Post).filter(models.Post.id == post_id).first():
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(models.Like).filter(
        models.Like.post_id == post_id,
        models.Like.user_id == current_user.id
    ).first()

    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": "Like removed"}
    else:
        new_like = models.Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Post liked"}

@router.get("/post/{post_id}", response_model=List[schemas.LikeResponse])
def get_post_likes(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all likes for a specific post with user details
    Returns:
    - List of likes with:
      - User information (id, username, email)
      - Like timestamp (if available)
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    likes = db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).options(
        joinedload(models.Like.user)  # Eager load user data
    ).all()
    
    return likes