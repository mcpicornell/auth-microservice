from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter


class TestUserServiceAdapter:
    @pytest.fixture
    def mock_auth_service(self):
        service = Mock()
        service.create_user = AsyncMock()
        service.login = AsyncMock()
        service.get_user = AsyncMock()
        service.get_user_by_email = AsyncMock()
        service.update_user = AsyncMock()
        return service

    @pytest.fixture
    def user_service_adapter(self, mock_auth_service):
        return UserServiceAdapter(mock_auth_service)

    def test_initialization(self, mock_auth_service):
        # Test that UserServiceAdapter initializes correctly
        adapter = UserServiceAdapter(mock_auth_service)
        assert adapter.auth_service == mock_auth_service

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service_adapter, mock_auth_service):
        # Arrange
        email = "test@example.com"
        username = "testuser"
        password = "password123"

        mock_result = Mock()
        mock_result.success = True
        mock_result.message = "User created successfully"
        mock_result.user = Mock()
        mock_result.user.id = uuid4()
        mock_result.user.email = email
        mock_result.user.username = username

        mock_auth_service.create_user.return_value = mock_result

        # Act
        result = await user_service_adapter.create_user(email, username, password)

        # Assert
        assert result.success is True
        assert result.message == "User created successfully"
        assert result.user == mock_result.user
        mock_auth_service.create_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_success(self, user_service_adapter, mock_auth_service):
        # Arrange
        email = "test@example.com"
        password = "password123"

        mock_result = Mock()
        mock_result.access_token = "access_token_123"
        mock_result.refresh_token = "refresh_token_123"
        mock_result.user_id = str(uuid4())
        mock_result.email = email
        mock_result.username = "testuser"
        mock_result.token_type = "bearer"

        mock_auth_service.login.return_value = mock_result

        # Act
        result = await user_service_adapter.login(email, password)

        # Assert
        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_123"
        assert result.email == email
        assert result.username == "testuser"
        assert result.token_type == "bearer"
        mock_auth_service.login.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_success(self, user_service_adapter, mock_auth_service):
        # Arrange
        user_id = uuid4()

        mock_result = Mock()
        mock_result.success = True
        mock_result.message = "User found"
        mock_result.user = Mock()
        mock_result.user.id = user_id
        mock_result.user.email = "test@example.com"

        mock_auth_service.get_user.return_value = mock_result

        # Act
        result = await user_service_adapter.get_user(user_id)

        # Assert
        assert result.success is True
        assert result.message == "User found"
        assert result.user == mock_result.user
        mock_auth_service.get_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self, user_service_adapter, mock_auth_service
    ):
        # Arrange
        email = "test@example.com"

        mock_result = Mock()
        mock_result.success = True
        mock_result.message = "User found"
        mock_result.user = Mock()
        mock_result.user.id = uuid4()
        mock_result.user.email = email

        mock_auth_service.get_user_by_email.return_value = mock_result

        # Act
        result = await user_service_adapter.get_user_by_email(email)

        # Assert
        assert result.success is True
        assert result.message == "User found"
        assert result.user == mock_result.user
        mock_auth_service.get_user_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_service_adapter, mock_auth_service):
        # Arrange
        user_id = uuid4()
        email = "updated@example.com"
        username = "updateduser"

        mock_result = Mock()
        mock_result.success = True
        mock_result.message = "User updated successfully"
        mock_result.user = Mock()
        mock_result.user.id = user_id
        mock_result.user.email = email
        mock_result.user.username = username

        mock_auth_service.update_user.return_value = mock_result

        # Act
        result = await user_service_adapter.update_user(
            user_id, email=email, username=username
        )

        # Assert
        assert result.success is True
        assert result.message == "User updated successfully"
        assert result.user == mock_result.user
        mock_auth_service.update_user.assert_called_once()

    def test_dependency_injection(self, mock_auth_service):
        # Test that dependency is properly injected
        adapter = UserServiceAdapter(mock_auth_service)
        assert adapter.auth_service is mock_auth_service

    @pytest.mark.asyncio
    async def test_create_user_failure(self, user_service_adapter, mock_auth_service):
        # Arrange
        mock_result = Mock()
        mock_result.success = False
        mock_result.message = "Email already exists"
        mock_result.user = None

        mock_auth_service.create_user.return_value = mock_result

        # Act
        result = await user_service_adapter.create_user(
            "test@example.com", "testuser", "password123"
        )

        # Assert
        assert result.success is False
        assert result.message == "Email already exists"
        assert result.user is None
