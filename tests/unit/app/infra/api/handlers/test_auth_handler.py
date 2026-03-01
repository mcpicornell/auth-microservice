from unittest.mock import AsyncMock, Mock

import pytest

from src.app.infra.api.handlers.auth_handler import AuthHandler
from src.app.infra.api.schemas import (
    CreateUserRequest,
    LoginRequest,
)


class TestAuthHandler:
    @pytest.fixture
    def mock_user_service(self, mocker):
        service = Mock()
        service.create_user = AsyncMock()
        service.login = AsyncMock()
        return service

    @pytest.fixture
    def auth_handler(self, mock_user_service):
        return AuthHandler(mock_user_service)

    @pytest.fixture
    def sample_user_request(self):
        return CreateUserRequest(
            email="test@example.com",
            username="testuser",
            password="password123",
        )

    @pytest.fixture
    def sample_login_request(self):
        return LoginRequest(
            email="test@example.com",
            password="password123",
        )

    @pytest.mark.asyncio
    async def test_register_failure(
        self, auth_handler, mock_user_service, sample_user_request
    ):
        # Arrange
        mock_result = Mock()
        mock_result.success = False
        mock_result.message = "Email already exists"

        mock_user_service.create_user.return_value = mock_result

        # Act & Assert
        with pytest.raises(Exception):  # Should raise HTTPException
            await auth_handler.register(sample_user_request)

    @pytest.mark.asyncio
    async def test_login_failure(
        self, auth_handler, mock_user_service, sample_login_request
    ):
        # Arrange
        mock_user_service.login.side_effect = ValueError("Invalid credentials")

        # Act & Assert
        with pytest.raises(Exception):  # Should raise HTTPException
            await auth_handler.login(sample_login_request)

    def test_router_setup(self, auth_handler):
        # Assert that router is properly configured
        assert auth_handler.router is not None
        assert auth_handler.router.prefix == "/auth"
        assert "authentication" in auth_handler.router.tags
