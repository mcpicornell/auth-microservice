from datetime import datetime, timezone
from uuid import uuid4

from src.app.infra.database.repositories.user_repository import (
    InfraCreateUserInput,
    InfraUserEntity,
)


class TestUserRepositoryDataclasses:
    """Simple tests for UserRepository dataclasses and basic functionality."""

    def test_infra_create_user_input_dataclass(self):
        """Test InfraCreateUserInput dataclass."""
        input_data = InfraCreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        assert input_data.email == "test@example.com"
        assert input_data.username == "testuser"
        assert input_data.password == "password123"
        assert hasattr(input_data, "__dataclass_fields__")

    def test_infra_user_entity_dataclass(self):
        """Test InfraUserEntity dataclass."""
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user_entity = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        assert isinstance(user_entity.id, type(user_id))
        assert isinstance(user_entity.email, str)
        assert isinstance(user_entity.username, str)
        assert isinstance(user_entity.hashed_password, str)
        assert isinstance(user_entity.is_active, bool)
        assert isinstance(user_entity.is_admin, bool)
        assert isinstance(user_entity.created_at, datetime)
        assert isinstance(user_entity.updated_at, datetime)
        assert hasattr(user_entity, "__dataclass_fields__")

    def test_infra_user_entity_equality(self):
        """Test InfraUserEntity equality."""
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user1 = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        user2 = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        assert user1 == user2

    def test_infra_user_entity_inequality(self):
        """Test InfraUserEntity inequality."""
        now = datetime.now(timezone.utc)

        user1 = InfraUserEntity(
            id=uuid4(),
            email="test1@example.com",
            username="testuser1",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        user2 = InfraUserEntity(
            id=uuid4(),
            email="test2@example.com",
            username="testuser2",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        assert user1 != user2

    def test_infra_user_entity_repr(self):
        """Test InfraUserEntity string representation."""
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user_entity = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        repr_str = repr(user_entity)
        assert "InfraUserEntity" in repr_str
        assert "test@example.com" in repr_str
        assert "testuser" in repr_str

    def test_infra_create_user_input_equality(self):
        """Test InfraCreateUserInput equality."""
        input1 = InfraCreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        input2 = InfraCreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        assert input1 == input2

    def test_infra_create_user_input_inequality(self):
        """Test InfraCreateUserInput inequality."""
        input1 = InfraCreateUserInput(
            email="test1@example.com", username="testuser1", password="password123"
        )

        input2 = InfraCreateUserInput(
            email="test2@example.com", username="testuser2", password="password456"
        )

        assert input1 != input2

    def test_infra_user_entity_field_mutability(self):
        """Test that InfraUserEntity fields are mutable."""
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user_entity = InfraUserEntity(
            id=user_id,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now,
        )

        # Test field mutation
        original_email = user_entity.email
        user_entity.email = "modified@example.com"
        assert user_entity.email == "modified@example.com"
        assert user_entity.email != original_email

        original_is_active = user_entity.is_active
        user_entity.is_active = False
        assert user_entity.is_active is False
        assert user_entity.is_active != original_is_active

    def test_infra_create_user_input_field_mutability(self):
        """Test that InfraCreateUserInput fields are mutable."""
        input_data = InfraCreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        # Test field mutation
        original_email = input_data.email
        input_data.email = "modified@example.com"
        assert input_data.email == "modified@example.com"
        assert input_data.email != original_email
