from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: date
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str