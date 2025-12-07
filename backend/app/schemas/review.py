from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(..., ge=1, le=5)  
    comment: str = Field(..., min_length=1, max_length=500)

class ReviewUpdate(BaseModel):
    rating: int = Field(None, ge=1, le=5)
    comment: str = Field(None, min_length=1, max_length=500)

class UserInReview(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    comment: str
    created_at: Optional[datetime] = None
    user: Optional[UserInReview] = None
    
    class Config:
        from_attributes = True

class ReviewWithUser(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    comment: str
    created_at: Optional[datetime] = None
    user: UserInReview
    
    class Config:
        from_attributes = True