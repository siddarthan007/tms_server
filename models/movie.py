from models.base import BaseModel
from typing import Optional

class Movie(BaseModel):
    movie_id: int
    title: str
    genre: Optional[str] = None
    language: Optional[str] = None
    duration: int
    created_at: str

class MovieCreate(BaseModel):
    title: str
    genre: Optional[str] = None
    language: Optional[str] = None
    duration: int