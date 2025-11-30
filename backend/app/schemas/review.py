from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(..., ge=1, le=5)  
    comment: str = Field(..., min_length=1, max_length=500)

class ReviewUpdate(BaseModel):
    rating: int = Field(None, ge=1, le=5)
    comment: str = Field(None, min_length=1, max_length=500)

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    comment: str
    
    class Config:
        from_attributes = True

class ReviewWithUser(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    comment: str
    user: dict  
    
    class Config:
        from_attributes = True