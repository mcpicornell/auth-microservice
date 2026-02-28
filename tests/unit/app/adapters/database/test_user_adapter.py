from uuid import uuid4

import pytest

from src.app.adapters.database.user_adapter import UserAdapter
from src.app.domain.entities.user import CreateUserInput, UserEntity


class TestUserAdapter:
    @pytest.fixture
    def mock_user_repository(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def mock_password_hasher(self, mocker):
        hasher = mocker.Mock()
        hasher.hash_password.return_value = "hashed_password"
        return hasher

    @pytest.fixture
    def user_adapter(self, mock_user_repository, mock_password_hasher):
        return UserAdapter(mock_user_repository, mock_password_hasher)

    @pytest.mark.asyncio
    async def test_get_by_email(self, user_adapter, mock_user_repository, mocker):
        email = "test@example.com"
        expected_user = UserEntity(
            id=uuid4(), email=email, username="test", hashed_password="hashed"
        )
        mock_user_repository.get_by_email = mocker.AsyncMock(return_value=expected_user)

        result = await user_adapter.get_by_email(email)

        mock_user_repository.get_by_email.assert_called_once_with(email)
        assert result == expected_user

    @pytest.mark.asyncio
    async def test_get_by_username(self, user_adapter, mock_user_repository, mocker):
        username = "testuser"
        expected_user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username=username,
            hashed_password="hashed",
        )
        mock_user_repository.get_by_username = mocker.AsyncMock(
            return_value=expected_user
        )

        result = await user_adapter.get_by_username(username)

        mock_user_repository.get_by_username.assert_called_once_with(username)
        assert result == expected_user

    @pytest.mark.asyncio
    async def test_get_by_id(self, user_adapter, mock_user_repository, mocker):
        user_id = uuid4()
        expected_user = UserEntity(
            id=user_id,
            email="test@example.com",
            username="test",
            hashed_password="hashed",
        )
        mock_user_repository.get_by_id = mocker.AsyncMock(return_value=expected_user)

        result = await user_adapter.get_by_id(user_id)

        mock_user_repository.get_by_id.assert_called_once_with(user_id)
        assert result == expected_user

    @pytest.mark.asyncio
    async def test_create(
        self, user_adapter, mock_user_repository, mock_password_hasher, mocker
    ):
        input_data = CreateUserInput(
            email="test@example.com", username="testuser", password="plain_password"
        )
        expected_user = UserEntity(
            id=uuid4(),
            email=input_data.email,
            username=input_data.username,
            hashed_password="hashed_password",
        )
        mock_user_repository.create = mocker.AsyncMock(return_value=expected_user)

        result = await user_adapter.create(input_data)

        mock_password_hasher.hash_password.assert_called_once_with("plain_password")
        expected_create_input = CreateUserInput(
            email=input_data.email,
            username=input_data.username,
            password="hashed_password",
        )
        mock_user_repository.create.assert_called_once_with(expected_create_input)
        assert result == expected_user

    @pytest.mark.asyncio
    async def test_update(self, user_adapter, mock_user_repository, mocker):
        user = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="test",
            hashed_password="hashed",
        )
        updated_user = UserEntity(
            id=user.id,
            email="updated@example.com",
            username="updated",
            hashed_password="hashed",
        )
        mock_user_repository.update = mocker.AsyncMock(return_value=updated_user)

        result = await user_adapter.update(user)

        mock_user_repository.update.assert_called_once_with(user)
        assert result == updated_user

    @pytest.mark.asyncio
    async def test_delete(self, user_adapter, mock_user_repository, mocker):
        user_id = uuid4()
        mock_user_repository.delete = mocker.AsyncMock(return_value=True)

        result = await user_adapter.delete(user_id)

        mock_user_repository.delete.assert_called_once_with(user_id)
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_failure(self, user_adapter, mock_user_repository, mocker):
        user_id = uuid4()
        mock_user_repository.delete = mocker.AsyncMock(return_value=False)

        result = await user_adapter.delete(user_id)

        mock_user_repository.delete.assert_called_once_with(user_id)
        assert result is False
