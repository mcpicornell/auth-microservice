from unittest.mock import Mock

import pytest


def test_imports():

    assert True


def test_dataclass_creation():
    from uuid import uuid4

    from src.app.domain.entities.user import CreateUserInput, UserEntity

    input_data = CreateUserInput(
        email="test@example.com", username="testuser", password="password123"
    )
    assert input_data.email == "test@example.com"
    assert input_data.username == "testuser"

    user_id = uuid4()
    user = UserEntity(
        id=user_id,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
    )
    assert user.id == user_id
    assert user.email == "test@example.com"
    assert user.is_active == True


@pytest.mark.asyncio
async def test_service_creation():
    from src.app.domain.ports import (
        EventPublisherPort,
        TokenProviderPort,
        UserRepositoryPort,
    )
    from src.app.domain.services.auth_service import AuthService

    mock_user_repo = Mock(spec=UserRepositoryPort)
    mock_token_provider = Mock(spec=TokenProviderPort)
    mock_event_publisher = Mock(spec=EventPublisherPort)

    auth_service = AuthService(
        user_repository_port=mock_user_repo,
        token_provider_port=mock_token_provider,
        event_publisher_port=mock_event_publisher,
    )

    assert auth_service is not None
    assert auth_service._user_repository_port == mock_user_repo
    assert auth_service._token_provider_port == mock_token_provider
    assert auth_service._event_publisher_port == mock_event_publisher
