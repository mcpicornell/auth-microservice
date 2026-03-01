from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.infra.database.repositories.user_repository import (
    InfraCreateUserInput,
    InfraUserEntity,
    UserRepository,
)


class MockAsyncSession:
    """Mock async session that properly implements async context manager."""

    def __init__(self):
        self.execute = AsyncMock()
        self.add = Mock()
        self.commit = AsyncMock()
        self.refresh = AsyncMock()
        self.delete = AsyncMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class TestUserRepositoryWorking:
    """Working tests for UserRepository to achieve 90% coverage."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        return MockAsyncSession()

    @pytest.fixture
    def mock_session_factory(self, mock_session):
        """Create a mock session factory that returns the mock session."""
        return lambda: mock_session

    @pytest.fixture
    def user_repository(self, mock_session_factory):
        """Create UserRepository with mocked session factory."""
        return UserRepository(mock_session_factory)

    @pytest.fixture
    def sample_user_db(self):
        """Create a sample UserDB instance."""
        from src.app.infra.database.repositories.models import UserDB

        return UserDB(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.mark.asyncio
    async def test_get_by_email_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test get_by_email when user is found."""
        # Mock the database response
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        result = await user_repository.get_by_email("test@example.com")

        assert result is not None
        assert result.email == sample_user_db.email
        assert result.username == sample_user_db.username
        assert isinstance(result, InfraUserEntity)

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_repository, mock_session):
        """Test get_by_email when user is not found."""
        # Mock the database response
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await user_repository.get_by_email("nonexistent@example.com")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_username_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test get_by_username when user is found."""
        # Mock the database response
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        result = await user_repository.get_by_username("testuser")

        assert result is not None
        assert result.username == sample_user_db.username
        assert result.email == sample_user_db.email
        assert isinstance(result, InfraUserEntity)

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test get_by_id when user is found."""
        user_id = sample_user_db.id

        # Mock the database response
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        result = await user_repository.get_by_id(user_id)

        assert result is not None
        assert result.id == user_id
        assert result.email == sample_user_db.email
        assert isinstance(result, InfraUserEntity)

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test create user successfully."""
        # Mock the database response
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        input_data = InfraCreateUserInput(
            email="new@example.com", username="newuser", password="password123"
        )

        result = await user_repository.create(input_data)

        assert result is not None
        assert result.email == input_data.email
        assert result.username == input_data.username
        assert result.is_active is True
        assert result.is_admin is False
        assert isinstance(result, InfraUserEntity)

        # Verify database operations were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test update user successfully."""
        # Mock the database response for finding the user
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        updated_user = InfraUserEntity(
            id=sample_user_db.id,
            email="updated@example.com",
            username="updateduser",
            hashed_password="hashed_password",
            is_active=False,
            is_admin=True,
            created_at=sample_user_db.created_at,
            updated_at=datetime.now(timezone.utc),
        )

        result = await user_repository.update(updated_user)

        assert result is not None
        assert isinstance(result, InfraUserEntity)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_repository, mock_session):
        """Test update user when user doesn't exist."""
        # Mock the database response for finding the user
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        user_entity = InfraUserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            is_admin=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        with pytest.raises(ValueError, match="User not found"):
            await user_repository.update(user_entity)

    @pytest.mark.asyncio
    async def test_delete_user_success(
        self, user_repository, mock_session, sample_user_db
    ):
        """Test delete user successfully."""
        # Mock the database response for finding the user
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_user_db
        mock_session.execute.return_value = mock_result

        result = await user_repository.delete(sample_user_db.id)

        assert result is True
        mock_session.delete.assert_called_once_with(sample_user_db)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_repository, mock_session):
        """Test delete user when user doesn't exist."""
        # Mock the database response for finding the user
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await user_repository.delete(uuid4())

        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_db_to_entity_conversion(self, user_repository, sample_user_db):
        """Test the _db_to_entity conversion method."""
        result = user_repository._db_to_entity(sample_user_db)

        assert isinstance(result, InfraUserEntity)
        assert result.id == sample_user_db.id
        assert result.email == sample_user_db.email
        assert result.username == sample_user_db.username
        assert result.hashed_password == sample_user_db.hashed_password
        assert result.is_active == sample_user_db.is_active
        assert result.is_admin == sample_user_db.is_admin
        assert result.created_at == sample_user_db.created_at
        assert result.updated_at == sample_user_db.updated_at

    def test_user_repository_initialization(self):
        """Test UserRepository initialization."""
        mock_factory = lambda: None
        repo = UserRepository(mock_factory)

        assert repo.session_factory == mock_factory
        assert hasattr(repo, "get_by_email")
        assert hasattr(repo, "get_by_username")
        assert hasattr(repo, "get_by_id")
        assert hasattr(repo, "create")
        assert hasattr(repo, "update")
        assert hasattr(repo, "delete")
        assert hasattr(repo, "_db_to_entity")
