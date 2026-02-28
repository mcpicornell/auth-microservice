from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenEntity:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    user_id: Optional[str] = None


@dataclass
class CreateTokenInput:
    user_id: str
    email: str


@dataclass
class CreateTokenOutput:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


@dataclass
class DecodedToken:
    sub: str  # user_id
    email: str
    exp: int
    iat: int
    type: str
