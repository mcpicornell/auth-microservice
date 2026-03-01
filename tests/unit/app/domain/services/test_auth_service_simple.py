from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.domain.services.auth_service import AuthService


class TestAuthServiceBasic:
    @pytest.fixture
    def mock_user_repository(self):
        repo = Mock()
        repo.create = AsyncMock()
        repo.get_by_email = AsyncMock()
        repo.get_by_id = AsyncMock()
        repo.get_by_username = AsyncMock()
        return repo

    @pytest.fixture
    def mock_token_provider(self):
        provider = Mock()
        provider.create_access_token = Mock()
        provider.create_refresh_token = Mock()
        provider.verify_token = Mock()
        return provider

    @pytest.fixture
    def mock_event_publisher(self):
        publisher = Mock()
        publisher.publish = AsyncMock()
        return publisher

    @pytest.fixture
    def auth_service(
        self, mock_user_repository, mock_token_provider, mock_event_publisher
    ):
        return AuthService(
            mock_user_repository, mock_token_provider, mock_event_publisher
        )

    def test_initialization(
        self, mock_user_repository, mock_token_provider, mock_event_publisher
    ):
        # Test that AuthService initializes correctly
        service = AuthService(
            mock_user_repository, mock_token_provider, mock_event_publisher
        )

        assert service.user_repository == mock_user_repository
        assert service.token_provider == mock_token_provider
        assert service.event_publisher == mock_event_publisher

    @pytest.mark.asyncio
    async def test_get_user_success(self, auth_service, mock_user_repository):
        # Arrange
        user_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"

        mock_user_repository.get_by_id.return_value = mock_user

        # Act
        result = await auth_service.get_user(user_id)

        # Assert
        assert result.success is True
        assert result.message is None  # Success case has no message
        assert result.user == mock_user
        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, auth_service, mock_user_repository):
        # Arrange
        user_id = uuid4()
        mock_user_repository.get_by_id.return_value = None

        # Act
        result = await auth_service.get_user(user_id)

        # Assert
        assert result.success is False
        assert result.message == "User not found"
        assert result.user is None
        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, auth_service, mock_user_repository):
        # Arrange
        email = "test@example.com"

        mock_user = Mock()
        mock_user.id = uuid4()
        mock_user.email = email
        mock_user.username = "testuser"

        mock_user_repository.get_by_email.return_value = mock_user

        # Act
        result = await auth_service.get_user_by_email(email)

        # Assert
        assert result.success is True
        assert result.message is None  # Success case has no message
        assert result.user == mock_user
        mock_user_repository.get_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(
        self, auth_service, mock_user_repository
    ):
        # Arrange
        email = "test@example.com"
        mock_user_repository.get_by_email.return_value = None

        # Act
        result = await auth_service.get_user_by_email(email)

        # Assert
        assert result.success is False
        assert result.message == "User not found"
        assert result.user is None
        mock_user_repository.get_by_email.assert_called_once_with(email)
