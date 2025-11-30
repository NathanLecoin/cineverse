from pydantic import BaseModel

class WatchlistCreate(BaseModel):
    user_id: int
    movie_id: int

class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    
    class Config:
        from_attributes = True

class WatchlistWithMovie(BaseModel):
    id: int
    user_id: int
    movie_id: int
    movie: dict  
    
    class Config:
        from_attributes = True