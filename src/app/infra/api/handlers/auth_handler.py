from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter
from src.app.infra.api.dto.responses import CreateUserResponse
from src.app.infra.api.schemas import (
    CreateUserRequest,
    LoginRequest,
    LoginResponse,
)


class AuthHandler:
    def __init__(self, user_service: UserServiceAdapter):
        self.user_service = user_service
        self.router = APIRouter(prefix="/auth", tags=["authentication"])
        self._setup_routes()

    def _setup_routes(self):
        @self.router.post(
            "/register",
            response_model=CreateUserResponse,
            status_code=status.HTTP_201_CREATED,
        )
        async def register(input_data: CreateUserRequest) -> CreateUserResponse:
            try:
                result = await self.user_service.create_user(
                    email=input_data.email,
                    username=input_data.username,
                    password=input_data.password,
                )

                if not result.success:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
                    )

                return CreateUserResponse(
                    id=result.user.id,
                    email=result.user.email,
                    username=result.user.username,
                    is_active=result.user.is_active,
                    is_admin=result.user.is_admin,
                    created_at=result.user.created_at,
                    updated_at=result.user.updated_at,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                ) from e

        @self.router.post("/login", response_model=LoginResponse)
        async def login(input_data: LoginRequest) -> LoginResponse:
            try:
                result = await self.user_service.login(
                    email=input_data.email,
                    password=input_data.password,
                )

                return LoginResponse(**result.__dict__)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
                ) from e

        @self.router.get("/me")
        async def get_current_user() -> Dict[str, Any]:
            return {"message": "This endpoint requires JWT authentication"}
