from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserResponse:
    id: UUID
    email: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: str
    updated_at: str


@dataclass
class CreateUserResponse:
    success: bool
    message: str
    user: Optional[UserResponse] = None


@dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    username: str
    token_type: str


@dataclass
class GetUserResponse:
    success: bool
    message: str
    user: Optional[UserResponse] = None


@dataclass
class UpdateUserResponse:
    success: bool
    message: str
    user: Optional[UserResponse] = None
