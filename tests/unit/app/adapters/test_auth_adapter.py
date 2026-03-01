from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.app.adapters.auth_adapter import AuthAdapter, UserEntityMapperPort
from src.app.domain.entities.user import (
    UserEntity,
)
from src.app.domain.services.auth_service import AuthService


class TestAuthAdapter:
    @pytest.fixture
    def mock_auth_service(self, mocker):
        return mocker.Mock(spec=AuthService)

    @pytest.fixture
    def mock_entity_mapper(self, mocker):
        return mocker.Mock(spec=UserEntityMapperPort)

    @pytest.fixture
    def auth_adapter(self, mock_auth_service, mock_entity_mapper):
        return AuthAdapter(mock_auth_service, mock_entity_mapper)

    @pytest.fixture
    def sample_user_entity(self):
        return UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, auth_adapter, mock_auth_service, mock_entity_mapper, sample_user_entity
    ):
        # Arrange
        mock_auth_service.create_user.return_value = Mock(
            success=True,
            message="User created successfully",
            user=sample_user_entity,
        )
        mock_entity_mapper.entity_to_dict.return_value = {
            "id": str(sample_user_entity.id),
            "email": sample_user_entity.email,
            "username": sample_user_entity.username,
            "is_active": sample_user_entity.is_active,
            "is_admin": sample_user_entity.is_admin,
            "created_at": sample_user_entity.created_at,
            "updated_at": sample_user_entity.updated_at,
        }

        # Act
        result = await auth_adapter.create_user(
            "test@example.com", "testuser", "password123"
        )

        # Assert
        assert result.success is True
        assert result.message == "User created successfully"
        assert result.user is not None
        assert result.user.email == "test@example.com"
        mock_auth_service.create_user.assert_called_once()
        mock_entity_mapper.entity_to_dict.assert_called_once_with(sample_user_entity)

    @pytest.mark.asyncio
    async def test_create_user_failure(self, auth_adapter, mock_auth_service):
        # Arrange
        mock_auth_service.create_user.return_value = Mock(
            success=False,
            message="Email already exists",
        )

        # Act
        result = await auth_adapter.create_user(
            "test@example.com", "testuser", "password123"
        )

        # Assert
        assert result.success is False
        assert result.message == "Email already exists"
        assert result.user is None
        mock_auth_service.create_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_success(
        self, auth_adapter, mock_auth_service, sample_user_entity
    ):
        # Arrange
        mock_auth_service.login.return_value = Mock(
            access_token="access_token_123",
            refresh_token="refresh_token_123",
            user=sample_user_entity,
            token_type="bearer",
        )

        # Act
        result = await auth_adapter.login("test@example.com", "password123")

        # Assert
        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_123"
        assert result.user_id == str(sample_user_entity.id)
        assert result.email == sample_user_entity.email
        assert result.username == sample_user_entity.username
        assert result.token_type == "bearer"
        mock_auth_service.login.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_success(
        self, auth_adapter, mock_auth_service, mock_entity_mapper, sample_user_entity
    ):
        # Arrange
        mock_auth_service.get_user.return_value = Mock(
            success=True,
            message="User found",
            user=sample_user_entity,
        )
        mock_entity_mapper.entity_to_dict.return_value = {
            "id": str(sample_user_entity.id),
            "email": sample_user_entity.email,
            "username": sample_user_entity.username,
            "is_active": sample_user_entity.is_active,
            "is_admin": sample_user_entity.is_admin,
            "created_at": sample_user_entity.created_at,
            "updated_at": sample_user_entity.updated_at,
        }

        # Act
        result = await auth_adapter.get_user(sample_user_entity.id)

        # Assert
        assert result.success is True
        assert result.user is not None
        assert result.user.email == "test@example.com"
        mock_auth_service.get_user.assert_called_once_with(sample_user_entity.id)
        mock_entity_mapper.entity_to_dict.assert_called_once_with(sample_user_entity)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, auth_adapter, mock_auth_service):
        # Arrange
        user_id = uuid4()
        mock_auth_service.get_user.return_value = Mock(
            success=False,
            message="User not found",
        )

        # Act
        result = await auth_adapter.get_user(user_id)

        # Assert
        assert result.success is False
        assert result.message == "User not found"
        assert result.user is None
        mock_auth_service.get_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self, auth_adapter, mock_auth_service, mock_entity_mapper, sample_user_entity
    ):
        # Arrange
        mock_auth_service.get_user_by_email.return_value = Mock(
            success=True,
            message="User found",
            user=sample_user_entity,
        )
        mock_entity_mapper.entity_to_dict.return_value = {
            "id": str(sample_user_entity.id),
            "email": sample_user_entity.email,
            "username": sample_user_entity.username,
            "is_active": sample_user_entity.is_active,
            "is_admin": sample_user_entity.is_admin,
            "created_at": sample_user_entity.created_at,
            "updated_at": sample_user_entity.updated_at,
        }

        # Act
        result = await auth_adapter.get_user_by_email("test@example.com")

        # Assert
        assert result.success is True
        assert result.user is not None
        assert result.user.email == "test@example.com"
        mock_auth_service.get_user_by_email.assert_called_once_with("test@example.com")
        mock_entity_mapper.entity_to_dict.assert_called_once_with(sample_user_entity)

    @pytest.mark.asyncio
    async def test_update_user_success(
        self, auth_adapter, mock_auth_service, mock_entity_mapper, sample_user_entity
    ):
        # Arrange
        mock_auth_service.update_user.return_value = Mock(
            success=True,
            message="User updated successfully",
            user=sample_user_entity,
        )
        mock_entity_mapper.entity_to_dict.return_value = {
            "id": str(sample_user_entity.id),
            "email": sample_user_entity.email,
            "username": sample_user_entity.username,
            "is_active": sample_user_entity.is_active,
            "is_admin": sample_user_entity.is_admin,
            "created_at": sample_user_entity.created_at,
            "updated_at": sample_user_entity.updated_at,
        }

        # Act
        result = await auth_adapter.update_user(
            sample_user_entity.id,
            email="newemail@example.com",
            username="newuser",
        )

        # Assert
        assert result.success is True
        assert result.message == "User updated successfully"
        assert result.user is not None
        assert result.user.email == "test@example.com"  # Original user data from mock
        mock_auth_service.update_user.assert_called_once()
        mock_entity_mapper.entity_to_dict.assert_called_once_with(sample_user_entity)

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, auth_adapter, mock_auth_service):
        # Arrange
        user_id = uuid4()
        mock_auth_service.update_user.return_value = Mock(
            success=False,
            message="User not found",
        )

        # Act
        result = await auth_adapter.update_user(user_id, email="newemail@example.com")

        # Assert
        assert result.success is False
        assert result.message == "User not found"
        assert result.user is None
        mock_auth_service.update_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, auth_adapter, mock_auth_service):
        # Arrange
        mock_auth_service.get_user_by_email.return_value = Mock(
            success=False,
            message="User not found",
        )

        # Act
        result = await auth_adapter.get_user_by_email("nonexistent@example.com")

        # Assert
        assert result.success is False
        assert result.message == "User not found"
        assert result.user is None
        mock_auth_service.get_user_by_email.assert_called_once_with(
            "nonexistent@example.com"
        )
