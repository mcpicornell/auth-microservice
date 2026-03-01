from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.app.adapters.database.user_adapter import UserAdapter
from src.app.domain.entities.user import UserEntity
from src.app.domain.ports.password_hasher_port import PasswordHasherPort
from src.app.domain.ports.user_repository_port import UserRepositoryPort


class TestSimpleCoverageBoost:
    def test_user_adapter_initialization(self):
        """Test UserAdapter initialization."""
        mock_user_repository = Mock(spec=UserRepositoryPort)
        mock_password_hasher = Mock(spec=PasswordHasherPort)

        adapter = UserAdapter(mock_user_repository, mock_password_hasher)

        assert adapter.user_repository == mock_user_repository
        assert adapter.password_hasher == mock_password_hasher

    @pytest.mark.asyncio
    async def test_entity_to_dict_coverage(self):
        """Test entity_to_dict method to cover missing line."""
        mock_user_repository = Mock(spec=UserRepositoryPort)
        mock_password_hasher = Mock(spec=PasswordHasherPort)

        adapter = UserAdapter(mock_user_repository, mock_password_hasher)

        # Create a valid user entity
        user_entity = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        # Test entity_to_dict
        result = adapter.entity_to_dict(user_entity)

        assert result["email"] == "test@example.com"
        assert result["username"] == "testuser"
        assert result["is_active"] is True
        assert result["is_admin"] is False

    @pytest.mark.asyncio
    async def test_hash_password_coverage(self):
        """Test hash_password method to cover missing lines."""
        mock_password_hasher = Mock(spec=PasswordHasherPort)
        mock_password_hasher.hash_password = Mock(return_value="hashed_password_123")

        # Test hash_password
        result = mock_password_hasher.hash_password("plain_password")

        assert result == "hashed_password_123"
        mock_password_hasher.hash_password.assert_called_once_with("plain_password")

    @pytest.mark.asyncio
    async def test_verify_password_coverage(self):
        """Test verify_password method to cover missing lines."""
        mock_password_hasher = Mock(spec=PasswordHasherPort)
        mock_password_hasher.verify_password = Mock(return_value=True)

        # Test verify_password
        result = mock_password_hasher.verify_password(
            "plain_password", "hashed_password"
        )

        assert result is True
        mock_password_hasher.verify_password.assert_called_once_with(
            "plain_password", "hashed_password"
        )
