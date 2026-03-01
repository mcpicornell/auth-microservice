"""Simple tests to improve coverage for auth_service.py"""

from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.domain.entities.user import (
    CreateUserInput,
    CreateUserOutput,
    GetUserOutput,
    LoginInput,
    UpdateUserInput,
    UpdateUserOutput,
)
from src.app.domain.services.auth_service import AuthService


class TestAuthServiceSimpleCoverage:
    @pytest.fixture
    def mock_user_repository(self):
        return AsyncMock()

    @pytest.fixture
    def mock_token_provider(self):
        return AsyncMock()

    @pytest.fixture
    def mock_event_publisher(self):
        return AsyncMock()

    @pytest.fixture
    def auth_service(
        self, mock_user_repository, mock_token_provider, mock_event_publisher
    ):
        return AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, auth_service, mock_user_repository, mock_event_publisher
    ):
        """Test successful user creation."""
        user_id = uuid4()
        input_data = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None

        mock_user_entity = Mock()
        mock_user_entity.id = user_id
        mock_user_entity.email = "test@example.com"
        mock_user_entity.username = "testuser"
        mock_user_repository.create.return_value = mock_user_entity

        result = await auth_service.create_user(input_data)

        assert isinstance(result, CreateUserOutput)
        assert result.success is True
        assert result.user == mock_user_entity
        mock_event_publisher.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, auth_service, mock_user_repository):
        """Test user creation with existing email."""
        input_data = CreateUserInput(
            email="existing@example.com", username="testuser", password="password123"
        )

        existing_user = Mock()
        mock_user_repository.get_by_email.return_value = existing_user

        result = await auth_service.create_user(input_data)

        assert isinstance(result, CreateUserOutput)
        assert result.success is False
        assert result.message == "Email already registered"

    @pytest.mark.asyncio
    async def test_create_user_username_exists(
        self, auth_service, mock_user_repository
    ):
        """Test user creation with existing username."""
        input_data = CreateUserInput(
            email="test@example.com", username="existinguser", password="password123"
        )

        mock_user_repository.get_by_email.return_value = None
        existing_user = Mock()
        mock_user_repository.get_by_username.return_value = existing_user

        result = await auth_service.create_user(input_data)

        assert isinstance(result, CreateUserOutput)
        assert result.success is False
        assert result.message == "Username already taken"

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, auth_service, mock_user_repository):
        """Test login with non-existent user."""
        input_data = LoginInput(email="nonexistent@example.com", password="password123")
        mock_user_repository.get_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid credentials"):
            await auth_service.login(input_data)

    @pytest.mark.asyncio
    async def test_get_user_found(self, auth_service, mock_user_repository):
        """Test successful user retrieval."""
        user_id = uuid4()
        mock_user = Mock()
        mock_user_repository.get_by_id.return_value = mock_user

        result = await auth_service.get_user(user_id)

        assert isinstance(result, GetUserOutput)
        assert result.success is True
        assert result.user == mock_user

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, auth_service, mock_user_repository):
        """Test user retrieval when user not found."""
        user_id = uuid4()
        mock_user_repository.get_by_id.return_value = None

        result = await auth_service.get_user(user_id)

        assert isinstance(result, GetUserOutput)
        assert result.success is False
        assert result.message == "User not found"

    @pytest.mark.asyncio
    async def test_get_user_by_email_found(self, auth_service, mock_user_repository):
        """Test successful user retrieval by email."""
        email = "test@example.com"
        mock_user = Mock()
        mock_user_repository.get_by_email.return_value = mock_user

        result = await auth_service.get_user_by_email(email)

        assert isinstance(result, GetUserOutput)
        assert result.success is True
        assert result.user == mock_user

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(
        self, auth_service, mock_user_repository
    ):
        """Test user retrieval by email when user not found."""
        email = "nonexistent@example.com"
        mock_user_repository.get_by_email.return_value = None

        result = await auth_service.get_user_by_email(email)

        assert isinstance(result, GetUserOutput)
        assert result.success is False
        assert result.message == "User not found"

    @pytest.mark.asyncio
    async def test_update_user_success(
        self, auth_service, mock_user_repository, mock_event_publisher
    ):
        """Test successful user update."""
        user_id = uuid4()
        input_data = UpdateUserInput(
            id=user_id,
            email="updated@example.com",
            username="updateduser",
            is_active=True,
            is_admin=False,
        )

        mock_existing_user = Mock()
        mock_existing_user.id = user_id
        mock_existing_user.email = "old@example.com"
        mock_existing_user.username = "olduser"
        mock_user_repository.get_by_id.return_value = mock_existing_user

        # Mock email and username checks to return None (no conflicts)
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None

        mock_updated_user = Mock()
        mock_updated_user.id = user_id
        mock_updated_user.email = "updated@example.com"
        mock_updated_user.username = "updateduser"
        mock_user_repository.update.return_value = mock_updated_user

        result = await auth_service.update_user(input_data)

        assert isinstance(result, UpdateUserOutput)
        assert result.success is True
        assert result.user == mock_updated_user
        mock_event_publisher.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, auth_service, mock_user_repository):
        """Test user update when user not found."""
        user_id = uuid4()
        input_data = UpdateUserInput(id=user_id, email="updated@example.com")
        mock_user_repository.get_by_id.return_value = None

        result = await auth_service.update_user(input_data)

        assert isinstance(result, UpdateUserOutput)
        assert result.success is False
        assert result.message == "User not found"

    @pytest.mark.asyncio
    async def test_update_user_email_conflict(self, auth_service, mock_user_repository):
        """Test user update with email conflict."""
        user_id = uuid4()
        input_data = UpdateUserInput(id=user_id, email="existing@example.com")

        mock_existing_user = Mock()
        mock_existing_user.id = user_id
        mock_existing_user.email = "old@example.com"
        mock_user_repository.get_by_id.return_value = mock_existing_user

        mock_email_user = Mock()
        mock_user_repository.get_by_email.return_value = mock_email_user

        result = await auth_service.update_user(input_data)

        assert isinstance(result, UpdateUserOutput)
        assert result.success is False
        assert result.message == "Email already registered"

    @pytest.mark.asyncio
    async def test_update_user_username_conflict(
        self, auth_service, mock_user_repository
    ):
        """Test user update with username conflict."""
        user_id = uuid4()
        input_data = UpdateUserInput(id=user_id, username="existinguser")

        mock_existing_user = Mock()
        mock_existing_user.id = user_id
        mock_existing_user.username = "olduser"
        mock_user_repository.get_by_id.return_value = mock_existing_user

        mock_user_repository.get_by_email.return_value = None
        mock_username_user = Mock()
        mock_user_repository.get_by_username.return_value = mock_username_user

        result = await auth_service.update_user(input_data)

        assert isinstance(result, UpdateUserOutput)
        assert result.success is False
        assert result.message == "Username already taken"

    @pytest.mark.asyncio
    async def test_update_user_partial_update(
        self, auth_service, mock_user_repository, mock_event_publisher
    ):
        """Test user update with partial data."""
        user_id = uuid4()
        input_data = UpdateUserInput(id=user_id, is_active=False)

        mock_existing_user = Mock()
        mock_existing_user.id = user_id
        mock_existing_user.is_active = True
        mock_user_repository.get_by_id.return_value = mock_existing_user

        mock_updated_user = Mock()
        mock_updated_user.id = user_id
        mock_user_repository.update.return_value = mock_updated_user

        result = await auth_service.update_user(input_data)

        assert isinstance(result, UpdateUserOutput)
        assert result.success is True
        assert result.user == mock_updated_user
        # Verify only is_active was updated
        assert mock_existing_user.is_active is False
