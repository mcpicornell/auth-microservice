from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.domain.entities.user import (
    CreateUserInput,
    LoginInput,
    UpdateUserInput,
    UserEntity,
)
from src.app.domain.ports import (
    EventPublisherPort,
    TokenProviderPort,
    UserRepositoryPort,
)
from src.app.domain.services.auth_service import AuthService


class TestAuthService:
    @pytest.mark.asyncio
    async def test_create_user_success(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        create_input = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        sample_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.return_value = sample_user

        result = await auth_service.create_user(create_input)

        assert result.id == sample_user.id
        assert result.email == "test@example.com"
        assert result.username == "testuser"
        assert result.is_active is True
        assert result.is_admin is False

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.get_by_username.assert_called_once_with("testuser")
        mock_user_repository.create.assert_called_once()
        mock_event_publisher.publish.assert_called_once_with(
            "user.created",
            {
                "user_id": str(sample_user.id),
                "email": sample_user.email,
                "username": sample_user.username,
            },
        )

    @pytest.mark.asyncio
    async def test_create_user_email_already_exists(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        create_input = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="existinguser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = existing_user

        try:
            await auth_service.create_user(create_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Email already registered" in str(e)

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_username_already_exists(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        create_input = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        existing_user = UserEntity(
            id=uuid4(),
            email="other@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = existing_user

        try:
            await auth_service.create_user(create_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Username already taken" in str(e)

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.get_by_username.assert_called_once_with("testuser")
        mock_user_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_success(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        login_input = LoginInput(email="test@example.com", password="password123")

        sample_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = sample_user

        mock_access_output = AsyncMock()
        mock_access_output.access_token = "access_token"
        mock_refresh_output = AsyncMock()
        mock_refresh_output.refresh_token = "refresh_token"

        mock_token_provider.create_access_token.return_value = mock_access_output
        mock_token_provider.create_refresh_token.return_value = mock_refresh_output

        result = await auth_service.login(login_input)

        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"
        assert result.token_type == "bearer"
        assert result.user_id == sample_user.id
        assert result.email == sample_user.email
        assert result.username == sample_user.username

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_token_provider.create_access_token.assert_called_once()
        mock_token_provider.create_refresh_token.assert_called_once()
        mock_event_publisher.publish.assert_called_once_with(
            "user.login",
            {
                "user_id": str(sample_user.id),
                "email": sample_user.email,
            },
        )

    @pytest.mark.asyncio
    async def test_login_user_not_found(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        login_input = LoginInput(
            email="nonexistent@example.com", password="password123"
        )

        mock_user_repository.get_by_email.return_value = None

        try:
            await auth_service.login(login_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid credentials" in str(e)

        mock_user_repository.get_by_email.assert_called_once_with(
            "nonexistent@example.com"
        )
        mock_token_provider.create_access_token.assert_not_called()
        mock_token_provider.create_refresh_token.assert_not_called()
        mock_event_publisher.publish.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        user_id = uuid4()
        sample_user = UserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = sample_user

        result = await auth_service.get_user_by_id(user_id)

        assert result.id == user_id
        assert result.email == "test@example.com"
        assert result.username == "testuser"

        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        user_id = uuid4()
        mock_user_repository.get_by_id.return_value = None

        try:
            await auth_service.get_user_by_id(user_id)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "User not found" in str(e)

        mock_user_repository.get_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        sample_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = sample_user

        result = await auth_service.get_user_by_email("test@example.com")

        assert result.id == sample_user.id
        assert result.email == "test@example.com"
        assert result.username == "testuser"

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        mock_user_repository.get_by_email.return_value = None

        try:
            await auth_service.get_user_by_email("nonexistent@example.com")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "User not found" in str(e)

        mock_user_repository.get_by_email.assert_called_once_with(
            "nonexistent@example.com"
        )

    @pytest.mark.asyncio
    async def test_update_user_success(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(email="newemail@example.com", is_active=False)

        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        updated_user = UserEntity(
            id=existing_user.id,
            email="newemail@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=False,
        )

        mock_user_repository.get_by_id.return_value = existing_user
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.update.return_value = updated_user

        result = await auth_service.update_user(existing_user.id, update_input)

        assert result.email == "newemail@example.com"
        assert result.is_active is False

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.update.assert_called_once()
        mock_event_publisher.publish.assert_called_once_with(
            "user.updated",
            {
                "user_id": str(updated_user.id),
                "email": updated_user.email,
                "username": updated_user.username,
            },
        )

    @pytest.mark.asyncio
    async def test_update_user_not_found(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(email="newemail@example.com")
        user_id = uuid4()

        mock_user_repository.get_by_id.return_value = None

        try:
            await auth_service.update_user(user_id, update_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "User not found" in str(e)

        mock_user_repository.get_by_id.assert_called_once_with(user_id)
        mock_user_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_email_already_exists(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(email="existing@example.com")
        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )
        other_user = UserEntity(
            id=uuid4(),
            email="existing@example.com",
            username="otheruser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = existing_user
        mock_user_repository.get_by_email.return_value = other_user

        try:
            await auth_service.update_user(existing_user.id, update_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Email already registered" in str(e)

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.get_by_email.assert_called_once_with(
            "existing@example.com"
        )
        mock_user_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_username_already_exists(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(username="existinguser")
        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )
        other_user = UserEntity(
            id=uuid4(),
            email="other@example.com",
            username="existinguser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = existing_user
        mock_user_repository.get_by_username.return_value = other_user

        try:
            await auth_service.update_user(existing_user.id, update_input)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Username already taken" in str(e)

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.get_by_username.assert_called_once_with("existinguser")
        mock_user_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_same_email_no_conflict(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(email="test@example.com")
        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = existing_user
        mock_user_repository.get_by_email.return_value = existing_user
        mock_user_repository.update.return_value = existing_user

        result = await auth_service.update_user(existing_user.id, update_input)

        assert result.email == "test@example.com"

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.get_by_email.assert_not_called()
        mock_user_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_same_username_no_conflict(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        update_input = UpdateUserInput(username="testuser")
        existing_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = existing_user
        mock_user_repository.get_by_username.return_value = existing_user
        mock_user_repository.update.return_value = existing_user

        result = await auth_service.update_user(existing_user.id, update_input)

        assert result.username == "testuser"

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.get_by_username.assert_not_called()
        mock_user_repository.update.assert_called_once()
