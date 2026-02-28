from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from src.app.domain.services.auth_service import AuthService
from src.app.domain.entities.user import CreateUserInput, CreateUserOutput, LoginInput, LoginOutput


class AuthHandler:
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/auth", tags=["authentication"])
        self._setup_routes()
    
    def _setup_routes(self):
        
        @self.router.post(
            "/register", 
            response_model=CreateUserOutput,
            status_code=status.HTTP_201_CREATED
        )
        async def register(input_data: CreateUserInput) -> CreateUserOutput:
            try:
                return await self.auth_service.create_user(input_data)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
        
        @self.router.post("/login", response_model=LoginOutput)
        async def login(input_data: LoginInput) -> LoginOutput:
            try:
                return await self.auth_service.login(input_data)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e)
                )
        
        @self.router.get("/me")
        async def get_current_user() -> Dict[str, Any]:
            return {"message": "This endpoint requires JWT authentication"}
