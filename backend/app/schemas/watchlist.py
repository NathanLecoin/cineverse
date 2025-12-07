from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.movie import MovieResponse

class WatchlistCreate(BaseModel):
    user_id: int
    movie_id: int

class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WatchlistWithMovie(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: Optional[datetime] = None
    movie: MovieResponse
    
    class Config:
        from_attributes = True