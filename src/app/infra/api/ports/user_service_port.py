from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.app.infra.api.dto.responses import (
    CreateUserResponse,
    GetUserResponse,
    LoginResponse,
    UpdateUserResponse,
)


class UserServicePort(ABC):
    @abstractmethod
    async def create_user(
        self, email: str, username: str, password: str
    ) -> CreateUserResponse:
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> LoginResponse:
        pass

    @abstractmethod
    async def get_user(self, user_id: UUID) -> GetUserResponse:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> GetUserResponse:
        pass

    @abstractmethod
    async def update_user(
        self,
        user_id: UUID,
        email: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
    ) -> UpdateUserResponse:
        pass
