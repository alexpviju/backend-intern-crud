from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

#  User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True


#  Auth Schemas 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#  Post Schemas 
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    image: Optional[str] = None 

class PostResponse(PostBase):
    id: int
    image: Optional[str] = None
    created_at: datetime
    author: UserResponse
    like_count: int
    comment_count: int
    class Config:
        orm_mode = True
        
class PostUpdate(BaseModel):
    title: str
    content: str
    image: Optional[str] = None
#  Comment Schemas 
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    user: UserResponse
    class Config:
        orm_mode = True

#  Like Schema 
class LikeResponse(BaseModel):
    id: int
    user: UserResponse
    class Config:
        orm_mode = True
class LikeCreate(BaseModel):
    post_id: int
    user_id: int 
