from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class DecodedToken(BaseModel):
    user_id: UUID
    email: str
    username: str
    is_admin: bool
    exp: datetime
    iat: datetime

    class Config:
        from_attributes = True
