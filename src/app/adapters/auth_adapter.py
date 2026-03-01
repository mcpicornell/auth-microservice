from typing import Optional, Protocol
from uuid import UUID

from src.app.domain.entities.user import (
    CreateUserInput,
    LoginInput,
    UpdateUserInput,
)
from src.app.domain.services.auth_service import AuthService
from src.app.infra.api.dto.responses import (
    CreateUserResponse,
    GetUserResponse,
    LoginResponse,
    UpdateUserResponse,
    UserResponse,
)


class UserEntityMapperPort(Protocol):
    def entity_to_dict(self, entity) -> dict: ...


class AuthAdapterPort(Protocol):
    async def create_user(
        self, email: str, username: str, password: str
    ) -> CreateUserResponse: ...
    async def login(self, email: str, password: str) -> LoginResponse: ...
    async def get_user(self, user_id: UUID) -> GetUserResponse: ...
    async def get_user_by_email(self, email: str) -> GetUserResponse: ...
    async def update_user(
        self,
        user_id: UUID,
        email: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
    ) -> UpdateUserResponse: ...


class AuthAdapter(AuthAdapterPort):
    def __init__(self, auth_service: AuthService, entity_mapper: UserEntityMapperPort):
        self.auth_service = auth_service
        self.entity_mapper = entity_mapper

    async def create_user(
        self, email: str, username: str, password: str
    ) -> CreateUserResponse:
        input_data = CreateUserInput(email=email, username=username, password=password)
        result = await self.auth_service.create_user(input_data)

        if not result.success:
            return CreateUserResponse(success=False, message=result.message)

        user_dict = self.entity_mapper.entity_to_dict(result.user)
        return CreateUserResponse(
            success=True, message=result.message, user=UserResponse(**user_dict)
        )

    async def login(self, email: str, password: str) -> LoginResponse:
        input_data = LoginInput(email=email, password=password)
        result = await self.auth_service.login(input_data)

        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            user_id=str(result.user.id),
            email=result.user.email,
            username=result.user.username,
            token_type=result.token_type,
        )

    async def get_user(self, user_id: UUID) -> GetUserResponse:
        result = await self.auth_service.get_user(user_id)

        if not result.success:
            return GetUserResponse(success=False, message=result.message)

        user_dict = self.entity_mapper.entity_to_dict(result.user)
        return GetUserResponse(
            success=True, message=result.message, user=UserResponse(**user_dict)
        )

    async def get_user_by_email(self, email: str) -> GetUserResponse:
        result = await self.auth_service.get_user_by_email(email)

        if not result.success:
            return GetUserResponse(success=False, message=result.message)

        user_dict = self.entity_mapper.entity_to_dict(result.user)
        return GetUserResponse(
            success=True, message=result.message, user=UserResponse(**user_dict)
        )

    async def update_user(
        self,
        user_id: UUID,
        email: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
    ) -> UpdateUserResponse:
        input_data = UpdateUserInput(
            id=user_id,
            email=email,
            username=username,
            is_active=is_active,
            is_admin=is_admin,
        )
        result = await self.auth_service.update_user(input_data)

        if not result.success:
            return UpdateUserResponse(success=False, message=result.message)

        user_dict = self.entity_mapper.entity_to_dict(result.user)
        return UpdateUserResponse(
            success=True, message=result.message, user=UserResponse(**user_dict)
        )
