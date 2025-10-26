from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str = None

class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    full_name: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str = None
    
    class Config:
        from_attributes = True
