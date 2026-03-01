from typing import Protocol

from passlib.context import CryptContext


class PasswordAdapterPort(Protocol):
    def hash_password(self, password: str) -> str: ...
    def verify_password(self, password: str, hashed_password: str) -> bool: ...


# pylint: disable=missing-class-docstring
class PasswordAdapter(PasswordAdapterPort):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
