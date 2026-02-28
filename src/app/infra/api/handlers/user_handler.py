from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.app.domain.entities.user import CreateUserInput, UpdateUserInput, UserResponse
from src.app.domain.services.auth_service import AuthService


class UserHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._setup_routes()

    def _setup_routes(self):

        @self.router.post(
            "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
        )
        async def create_user(create_input: CreateUserInput) -> UserResponse:
            try:
                user_output = await self.auth_service.create_user(create_input)
                return UserResponse(
                    id=user_output.id,
                    email=user_output.email,
                    username=user_output.username,
                    is_active=user_output.is_active,
                    is_admin=user_output.is_admin,
                    created_at=user_output.created_at,
                    updated_at=user_output.updated_at,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

        @self.router.patch("/{user_id}", response_model=UserResponse)
        async def update_user(
            user_id: UUID, update_input: UpdateUserInput
        ) -> UserResponse:
            try:
                updated_user = await self.auth_service.update_user(
                    user_id, update_input
                )
                return UserResponse(
                    id=updated_user.id,
                    email=updated_user.email,
                    username=updated_user.username,
                    is_active=updated_user.is_active,
                    is_admin=updated_user.is_admin,
                    created_at=updated_user.created_at,
                    updated_at=updated_user.updated_at,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )

        @self.router.get("/{user_id}", response_model=UserResponse)
        async def get_user(user_id: UUID) -> UserResponse:
            try:
                user = await self.auth_service.get_user_by_id(user_id)
                return UserResponse(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    is_active=user.is_active,
                    is_admin=user.is_admin,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                )

        @self.router.get("/email/{email}", response_model=UserResponse)
        async def get_user_by_email(email: str) -> UserResponse:
            try:
                user = await self.auth_service.get_user_by_email(email)
                return UserResponse(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    is_active=user.is_active,
                    is_admin=user.is_admin,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                )

        @self.router.get("/")
        async def list_users() -> Dict[str, Any]:
            return {"message": "User listing not yet implemented"}

        @self.router.delete("/{user_id}")
        async def delete_user(user_id: UUID) -> Dict[str, str]:
            return {"message": f"User deletion not yet implemented for {user_id}"}
