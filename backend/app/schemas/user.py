from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    id: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_online: bool = False
    last_seen: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
