import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form,status
from fastapi.responses import FileResponse,Response
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PostResponse)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    image_path = None
    if image:
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb+") as f:
            f.write(image.file.read())
        image_path = f"/uploads/{image.filename}"

    new_post = models.Post(
        title=title,
        content=content,
        image=image_path,
        author_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts



@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,  # Use the new schema
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update only provided fields
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a post by ID. Only the post author can delete their own post.
    """
    # 1. Get the post from database
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # 2. Check if post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    # 3. Verify the current user is the author
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    # 4. Delete the post (cascade will handle related likes/comments)
    db.delete(post)
    db.commit()
    
    # 5. Return no content (standard for DELETE operations)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    
    # Get the post from database
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # Check if post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    return post  