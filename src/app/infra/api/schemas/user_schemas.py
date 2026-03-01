from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: UUID
    email: EmailStr
    username: str
    token_type: str = "bearer"


class CreateUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
