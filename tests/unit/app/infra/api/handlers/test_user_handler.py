from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.app.domain.entities.event_message import EventMessage
from src.app.domain.entities.user import CreateUserInput, UpdateUserInput, UserEntity
from src.app.domain.ports import (
    EventPublisherPort,
    TokenProviderPort,
    UserRepositoryPort,
)
from src.app.domain.services.auth_service import AuthService
from src.app.infra.api.handlers.user_handler import UserHandler


class TestUserHandler:
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

        user_handler = UserHandler(auth_service)

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

        response = await user_handler.router.routes[0].endpoint(create_input)

        assert response.email == "test@example.com"
        assert response.username == "testuser"
        assert response.is_active is True
        assert response.is_admin is False

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.get_by_username.assert_called_once_with("testuser")
        mock_user_repository.create.assert_called_once()
        mock_event_publisher.publish.assert_called_once_with(
            EventMessage(
                event_name="user.created",
                data={
                    "user_id": str(sample_user.id),
                    "email": sample_user.email,
                    "username": sample_user.username,
                },
            )
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

        user_handler = UserHandler(auth_service)

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
            await user_handler.router.routes[0].endpoint(create_input)
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 400
            assert "Email already registered" in e.detail

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

        user_handler = UserHandler(auth_service)

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
            await user_handler.router.routes[0].endpoint(create_input)
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 400
            assert "Username already taken" in e.detail

        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.get_by_username.assert_called_once_with("testuser")
        mock_user_repository.create.assert_not_called()

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

        user_handler = UserHandler(auth_service)

        update_input = UpdateUserInput(email="newemail@example.com", is_active=False)

        sample_user = UserEntity(
            id=uuid4(),
            email="newemail@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=False,
        )

        mock_user_repository.get_by_id.return_value = sample_user
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.update.return_value = sample_user

        response = await user_handler.router.routes[1].endpoint(
            sample_user.id, update_input
        )

        assert response.email == "newemail@example.com"
        assert response.is_active is False

        mock_user_repository.get_by_id.assert_called_once_with(sample_user.id)
        mock_user_repository.update.assert_called_once()
        mock_event_publisher.publish.assert_called_once_with(
            EventMessage(
                event_name="user.updated",
                data={
                    "user_id": str(sample_user.id),
                    "email": sample_user.email,
                    "username": sample_user.username,
                },
            )
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

        user_handler = UserHandler(auth_service)

        update_input = UpdateUserInput(email="newemail@example.com")
        user_id = uuid4()

        mock_user_repository.get_by_id.return_value = None

        try:
            await user_handler.router.routes[1].endpoint(user_id, update_input)
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 400
            assert "User not found" in e.detail

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

        user_handler = UserHandler(auth_service)

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
            await user_handler.router.routes[1].endpoint(existing_user.id, update_input)
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 400
            assert "Email already registered" in e.detail

        mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)
        mock_user_repository.get_by_email.assert_called_once_with(
            "existing@example.com"
        )
        mock_user_repository.update.assert_not_called()

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

        user_handler = UserHandler(auth_service)

        user_id = uuid4()
        sample_user = UserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_id.return_value = sample_user

        response = await user_handler.router.routes[2].endpoint(user_id)

        assert response.id == user_id
        assert response.email == "test@example.com"
        assert response.username == "testuser"
        assert response.is_active is True
        assert response.is_admin is False

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

        user_handler = UserHandler(auth_service)

        user_id = uuid4()
        mock_user_repository.get_by_id.return_value = None

        try:
            await user_handler.router.routes[2].endpoint(user_id)
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 404
            assert "User not found" in e.detail

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

        user_handler = UserHandler(auth_service)

        sample_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        mock_user_repository.get_by_email.return_value = sample_user

        response = await user_handler.router.routes[3].endpoint("test@example.com")

        assert response.id == sample_user.id
        assert response.email == "test@example.com"
        assert response.username == "testuser"
        assert response.is_active is True
        assert response.is_admin is False

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

        user_handler = UserHandler(auth_service)

        mock_user_repository.get_by_email.return_value = None

        try:
            await user_handler.router.routes[3].endpoint("nonexistent@example.com")
            assert False, "Should have raised HTTPException"
        except HTTPException as e:
            assert e.status_code == 404
            assert "User not found" in e.detail

        mock_user_repository.get_by_email.assert_called_once_with(
            "nonexistent@example.com"
        )

    @pytest.mark.asyncio
    async def test_list_users_endpoint(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        user_handler = UserHandler(auth_service)

        response = await user_handler.router.routes[4].endpoint()

        assert response["message"] == "User listing not yet implemented"

    @pytest.mark.asyncio
    async def test_delete_user_endpoint(self):
        mock_user_repository = AsyncMock(spec=UserRepositoryPort)
        mock_token_provider = AsyncMock(spec=TokenProviderPort)
        mock_event_publisher = AsyncMock(spec=EventPublisherPort)

        auth_service = AuthService(
            user_repository=mock_user_repository,
            token_provider=mock_token_provider,
            event_publisher=mock_event_publisher,
        )

        user_handler = UserHandler(auth_service)

        user_id = uuid4()
        response = await user_handler.router.routes[5].endpoint(user_id)

        assert response["message"] == f"User deletion not yet implemented for {user_id}"
