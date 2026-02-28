from datetime import datetime, timezone
from uuid import uuid4

from src.app.domain.entities.user import CreateUserInput, UpdateUserInput, UserEntity


class TestUserEntity:
    def test_user_entity_creation(self):
        user_id = uuid4()
        created_at = datetime.now(timezone.utc)

        user = UserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=created_at,
            updated_at=created_at,
        )

        assert user.id == user_id
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.created_at == created_at
        assert user.updated_at == created_at

    def test_user_entity_default_values(self):
        user_id = uuid4()

        user = UserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )

        assert user.id == user_id
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_create_user_input_creation(self):
        create_input = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        assert create_input.email == "test@example.com"
        assert create_input.username == "testuser"
        assert create_input.password == "password123"

    def test_update_user_input_creation(self):
        update_input = UpdateUserInput(email="newemail@example.com", is_active=False)

        assert update_input.email == "newemail@example.com"
        assert update_input.is_active is False
        assert update_input.username is None
        assert update_input.is_admin is None

    def test_update_user_input_empty(self):
        update_input = UpdateUserInput()

        assert update_input.email is None
        assert update_input.username is None
        assert update_input.is_active is None
        assert update_input.is_admin is None
