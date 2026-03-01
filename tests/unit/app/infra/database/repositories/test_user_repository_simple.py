from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.app.infra.database.repositories.user_repository import UserRepository


class TestUserRepositoryBasic:
    @pytest.fixture
    def mock_session_factory(self):
        factory = Mock()
        return factory

    @pytest.fixture
    def user_repository(self, mock_session_factory):
        return UserRepository(mock_session_factory)

    def test_initialization(self, mock_session_factory):
        # Test that UserRepository initializes correctly
        repo = UserRepository(mock_session_factory)
        assert repo.session_factory == mock_session_factory

    def test_db_to_entity_conversion(self, user_repository):
        # Arrange
        user_id = uuid4()
        mock_user_db = Mock()
        mock_user_db.id = user_id
        mock_user_db.email = "test@example.com"
        mock_user_db.username = "testuser"
        mock_user_db.hashed_password = "hashed_password"
        mock_user_db.is_active = True
        mock_user_db.is_admin = False
        mock_user_db.created_at = "2023-01-01T00:00:00Z"
        mock_user_db.updated_at = "2023-01-01T00:00:00Z"

        # Act
        result = user_repository._db_to_entity(mock_user_db)

        # Assert
        assert result.id == user_id
        assert result.email == "test@example.com"
        assert result.username == "testuser"
        assert result.hashed_password == "hashed_password"
        assert result.is_active is True
        assert result.is_admin is False
        assert result.created_at == "2023-01-01T00:00:00Z"
        assert result.updated_at == "2023-01-01T00:00:00Z"

    def test_session_factory_is_called(self, mock_session_factory):
        # Test that the repository stores the session factory
        repo = UserRepository(mock_session_factory)
        assert repo.session_factory is mock_session_factory

    def test_infra_create_user_input_dataclass(self):
        # Test the InfraCreateUserInput dataclass
        from src.app.infra.database.repositories.user_repository import (
            InfraCreateUserInput,
        )

        input_data = InfraCreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        assert input_data.email == "test@example.com"
        assert input_data.username == "testuser"
        assert input_data.password == "password123"

    def test_infra_user_entity_dataclass(self):
        # Test the InfraUserEntity dataclass
        from datetime import datetime

        from src.app.infra.database.repositories.user_repository import InfraUserEntity

        user_id = uuid4()
        now = datetime.now()

        entity = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        assert entity.id == user_id
        assert entity.email == "test@example.com"
        assert entity.username == "testuser"
        assert entity.hashed_password == "hashed_password"
        assert entity.is_active is True
        assert entity.is_admin is False
        assert entity.created_at == now
        assert entity.updated_at == now
