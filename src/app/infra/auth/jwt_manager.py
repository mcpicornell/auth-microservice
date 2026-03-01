from datetime import datetime, timedelta, timezone
from typing import Protocol
from uuid import UUID

from jose import JWTError, jwt


class DecodedToken:
    def __init__(
        self, sub: str, email: str, exp: datetime, iat: datetime, token_type: str
    ):
        self.user_id = UUID(sub)
        self.email = email
        self.exp = exp
        self.iat = iat
        self.type = token_type


class JWTPort(Protocol):
    def create_access_token(self, user_id: str, email: str) -> str: ...
    def create_refresh_token(self, user_id: str, email: str) -> str: ...
    def decode_token(self, token: str) -> DecodedToken: ...
    def verify_token(self, token: str) -> bool: ...


class JWTManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_expire_minutes: int,
        refresh_expire_days: int,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_expire_minutes = access_expire_minutes
        self.refresh_expire_days = refresh_expire_days

    def create_access_token(self, user_id: str, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_expire_minutes
        )

        payload = {
            "sub": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_expire_days)

        payload = {
            "sub": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> DecodedToken:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return DecodedToken(
                sub=payload["sub"],
                email=payload["email"],
                exp=payload["exp"],
                iat=payload["iat"],
                token_type=payload["type"],
            )
        except JWTError as exc:
            raise ValueError("Invalid token") from exc

    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True
        except JWTError:
            return False
