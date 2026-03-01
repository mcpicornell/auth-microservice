from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.domain.entities.user import (
    CreateUserInput,
    CreateUserOutput,
    GetUserOutput,
    LoginInput,
    UserEntity,
)
from src.app.domain.ports.event_publisher_port import EventPublisherPort
from src.app.domain.ports.token_provider_port import TokenProviderPort
from src.app.domain.ports.user_repository_port import UserRepositoryPort
from src.app.domain.services.auth_service import AuthService


class TestAuthServiceSimple:
    @pytest.fixture
    def mock_user_repository(self):
        repo = Mock(spec=UserRepositoryPort)
        repo.get_by_email = AsyncMock()
        repo.get_by_username = AsyncMock()
        repo.create = AsyncMock()
        repo.get_by_id = AsyncMock()
        repo.update = AsyncMock()
        return repo

    @pytest.fixture
    def mock_token_provider(self):
        provider = Mock(spec=TokenProviderPort)
        return provider

    @pytest.fixture
    def mock_event_publisher(self):
        publisher = Mock(spec=EventPublisherPort)
        publisher.publish = AsyncMock()
        return publisher

    @pytest.fixture
    def auth_service(
        self, mock_user_repository, mock_token_provider, mock_event_publisher
    ):
        return AuthService(
            mock_user_repository, mock_token_provider, mock_event_publisher
        )

    @pytest.mark.asyncio
    async def test_login_user_not_found_raises_error(
        self, auth_service, mock_user_repository
    ):
        # Arrange
        email = "nonexistent@example.com"
        password = "password123"
        login_input = LoginInput(email=email, password=password)

        mock_user_repository.get_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid credentials"):
            await auth_service.login(login_input)

        mock_user_repository.get_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, auth_service, mock_user_repository):
        # Arrange
        email = "existing@example.com"
        username = "newuser"
        password = "password123"
        create_input = CreateUserInput(
            email=email, username=username, password=password
        )

        existing_user = UserEntity(
            id=uuid4(),
            email=email,
            username="existinguser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
        )

        mock_user_repository.get_by_email.return_value = existing_user

        # Act
        result = await auth_service.create_user(create_input)

        # Assert
        assert isinstance(result, CreateUserOutput)
        assert result.success is False
        assert result.message == "Email already registered"
        assert result.user is None
        mock_user_repository.get_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_create_user_username_exists(
        self, auth_service, mock_user_repository
    ):
        # Arrange
        email = "new@example.com"
        username = "existinguser"
        password = "password123"
        create_input = CreateUserInput(
            email=email, username=username, password=password
        )

        existing_user = UserEntity(
            id=uuid4(),
            email="existing@example.com",
            username=username,
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
        )

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = existing_user

        # Act
        result = await auth_service.create_user(create_input)

        # Assert
        assert isinstance(result, CreateUserOutput)
        assert result.success is False
        assert result.message == "Username already taken"
        assert result.user is None
        mock_user_repository.get_by_email.assert_called_once_with(email)
        mock_user_repository.get_by_username.assert_called_once_with(username)

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, auth_service, mock_user_repository):
        # Arrange
        user_id = uuid4()

        user_entity = UserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
        )

        mock_user_repository.get_by_id.return_value = user_entity

        # Act
        result = await auth_service.get_user(user_id)

        # Assert
        assert isinstance(result, GetUserOutput)
        assert result.success is True
        assert result.message is None
        assert result.user == user_entity
        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, auth_service, mock_user_repository):
        # Arrange
        user_id = uuid4()

        mock_user_repository.get_by_id.return_value = None

        # Act
        result = await auth_service.get_user(user_id)

        # Assert
        assert isinstance(result, GetUserOutput)
        assert result.success is False
        assert result.message is not None
        assert result.user is None
        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, auth_service, mock_user_repository):
        # Arrange
        email = "test@example.com"

        user_entity = UserEntity(
            id=uuid4(),
            email=email,
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
        )

        mock_user_repository.get_by_email.return_value = user_entity

        # Act
        result = await auth_service.get_user_by_email(email)

        # Assert
        assert isinstance(result, GetUserOutput)
        assert result.success is True
        assert result.message is None
        assert result.user == user_entity
        mock_user_repository.get_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(
        self, auth_service, mock_user_repository
    ):
        # Arrange
        email = "nonexistent@example.com"

        mock_user_repository.get_by_email.return_value = None

        # Act
        result = await auth_service.get_user_by_email(email)

        # Assert
        assert isinstance(result, GetUserOutput)
        assert result.success is False
        assert result.message is not None
        assert result.user is None
        mock_user_repository.get_by_email.assert_called_once_with(email)

    def test_auth_service_initialization(
        self, mock_user_repository, mock_token_provider, mock_event_publisher
    ):
        # Test that AuthService initializes correctly
        service = AuthService(
            mock_user_repository, mock_token_provider, mock_event_publisher
        )

        assert service.user_repository == mock_user_repository
        assert service.token_provider == mock_token_provider
        assert service.event_publisher == mock_event_publisher

    def test_auth_service_methods_exist(self, auth_service):
        # Test that all expected methods exist
        assert hasattr(auth_service, "create_user")
        assert hasattr(auth_service, "login")
        assert hasattr(auth_service, "get_user")
        assert hasattr(auth_service, "get_user_by_email")
        assert hasattr(auth_service, "update_user")

        # Test that methods are callable
        assert callable(auth_service.create_user)
        assert callable(auth_service.login)
        assert callable(auth_service.get_user)
        assert callable(auth_service.get_user_by_email)
        assert callable(auth_service.update_user)
