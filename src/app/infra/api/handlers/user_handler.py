from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter
from src.app.infra.api.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)


class UserHandler:
    def __init__(self, user_service: UserServiceAdapter):
        self.user_service = user_service
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._setup_routes()

    def _setup_routes(self):
        @self.router.post(
            "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
        )
        async def create_user(create_input: CreateUserRequest) -> UserResponse:
            try:
                result = await self.user_service.create_user(
                    email=create_input.email,
                    username=create_input.username,
                    password=create_input.password,
                )

                if not result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result["message"],
                    )

                return UserResponse(**result["data"])
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                ) from e

        @self.router.patch("/{user_id}", response_model=UserResponse)
        async def update_user(
            user_id: UUID, update_input: UpdateUserRequest
        ) -> UserResponse:
            try:
                result = await self.user_service.update_user(
                    user_id=user_id,
                    email=update_input.email,
                    username=update_input.username,
                    is_active=update_input.is_active,
                    is_admin=update_input.is_admin,
                )

                if not result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result["message"],
                    )

                return UserResponse(**result["data"])
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                ) from e

        @self.router.get("/{user_id}", response_model=UserResponse)
        async def get_user(user_id: UUID) -> UserResponse:
            try:
                result = await self.user_service.get_user(user_id)

                if not result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail=result["message"]
                    )

                return UserResponse(**result["data"])
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                ) from e

        @self.router.get("/email/{email}", response_model=UserResponse)
        async def get_user_by_email(email: str) -> UserResponse:
            try:
                result = await self.user_service.get_user_by_email(email)

                if not result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail=result["message"]
                    )

                return UserResponse(**result["data"])
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                ) from e

        @self.router.get("/")
        async def list_users() -> Dict[str, Any]:
            return {"message": "List users endpoint"}
