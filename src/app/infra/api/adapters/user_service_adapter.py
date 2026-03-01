from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.app.infra.api.dto.responses import (
    CreateUserResponse,
    GetUserResponse,
    LoginResponse,
    UpdateUserResponse,
)
from src.app.infra.api.ports.user_service_port import UserServicePort


class DomainAuthServiceInterface(ABC):
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


class UserServiceAdapter(UserServicePort):
    def __init__(self, auth_service: DomainAuthServiceInterface):
        self.auth_service = auth_service

    async def create_user(
        self, email: str, username: str, password: str
    ) -> CreateUserResponse:
        result = await self.auth_service.create_user(email, username, password)
        return result

    async def login(self, email: str, password: str) -> LoginResponse:
        result = await self.auth_service.login(email, password)
        return result

    async def get_user(self, user_id: UUID) -> GetUserResponse:
        result = await self.auth_service.get_user(user_id)
        return result

    async def get_user_by_email(self, email: str) -> GetUserResponse:
        result = await self.auth_service.get_user_by_email(email)
        return result

    async def update_user(
        self,
        user_id: UUID,
        email: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
    ) -> UpdateUserResponse:
        result = await self.auth_service.update_user(
            user_id, email, username, is_active, is_admin
        )
        return result
