"""
User models and schemas.
"""

from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user model."""
    email: str
    username: str


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserInDB(UserBase):
    """User in DB schema."""
    id: str
    hashed_password: str
    created_at: str


class UserResponse(UserBase):
    """User response schema."""
    id: str
    created_at: str


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload schema."""
    email: Optional[str] = None
    user_id: Optional[str] = None
