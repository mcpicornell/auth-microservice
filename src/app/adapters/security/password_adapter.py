from passlib.context import CryptContext

from src.app.domain.ports.password_hasher_port import PasswordHasherPort


# pylint: disable=missing-class-docstring
class PasswordAdapter(PasswordHasherPort):
    """Adapter for password hashing and verification using bcrypt."""

    def __init__(self):
        """Initialize the password adapter with bcrypt context."""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(password, hashed_password)
