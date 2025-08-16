from fastapi import FastAPI
from .routes import posts, comments, likes, users
from .database import Base, engine
from . import models,auth  

from fastapi.staticfiles import StaticFiles
from src.database import init_db

init_db()
app = FastAPI(title="Backend CRUD API")

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

