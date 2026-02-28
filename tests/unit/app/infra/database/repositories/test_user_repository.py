import pytest
from uuid import uuid4

from src.app.domain.entities.user import CreateUserInput, UpdateUserInput, UserEntity
from src.app.infra.database.repositories.user_repository import UserRepository


class TestUserRepository:
    
    @pytest.mark.asyncio
    async def test_user_repository_create(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        input_data = CreateUserInput(
            email="test@example.com", username="testuser", password="hashedpassword"
        )

        mock_user_db = mocker.Mock()
        mock_user_db.id = uuid4()
        mock_user_db.email = input_data.email
        mock_user_db.username = input_data.username
        mock_user_db.hashed_password = input_data.password
        mock_user_db.is_active = True
        mock_user_db.is_admin = False
        mock_user_db.created_at = mocker.Mock()
        mock_user_db.updated_at = mocker.Mock()

        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        result = await repository.create(input_data)

        assert isinstance(result, UserEntity)
        assert result.email == input_data.email
        assert result.username == input_data.username

    @pytest.mark.asyncio
    async def test_user_repository_get_by_email(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        await repository.get_by_email("test@example.com")

        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_user_repository_get_by_username(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        await repository.get_by_username("testuser")

        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_user_repository_get_by_id(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)
        user_id = uuid4()

        await repository.get_by_id(user_id)

        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_user_repository_update(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        user_entity = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password"
        )

        mock_user_db = mocker.Mock()
        mock_user_db.id = user_entity.id
        mock_user_db.email = user_entity.email
        mock_user_db.username = user_entity.username
        mock_user_db.hashed_password = user_entity.hashed_password

        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user_db
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        result = await repository.update(user_entity)

        assert isinstance(result, UserEntity)
        assert result.id == user_entity.id
        assert result.email == user_entity.email
        assert result.username == user_entity.username

    @pytest.mark.asyncio
    async def test_user_repository_update_not_found(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        user_entity = UserEntity(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password"
        )

        mock_session.execute.return_value.scalar_one_or_none.return_value = None

        try:
            await repository.update(user_entity)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "User not found" in str(e)

        mock_session.execute.assert_called_once()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_user_repository_delete(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)
        user_id = uuid4()

        await repository.delete(user_id)

        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_user_repository_list(self, mocker):
        mock_session_factory = mocker.Mock()
        mock_session = mocker.AsyncMock()
        mock_session_factory.return_value = mock_session

        repository = UserRepository(mock_session_factory)

        await repository.list()

        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_user_adapter_only_transforms_data(self, mocker):
        from src.app.adapters.database.user_adapter import UserAdapter
        from src.app.adapters.security.password_adapter import PasswordAdapter

        mock_user_repository = mocker.Mock(spec=UserRepository)
        mock_password_adapter = mocker.Mock(spec=PasswordAdapter)

        adapter = UserAdapter(mock_user_repository, mock_password_adapter)

        input_data = CreateUserInput(
            email="test@example.com", username="testuser", password="password123"
        )

        mock_password_adapter.hash_password.return_value = "hashed_password"
        mock_user_repository.create.return_value = mocker.Mock(spec=UserEntity)

        result = await adapter.create(input_data)

        mock_password_adapter.hash_password.assert_called_once_with("password123")
        mock_user_repository.create.assert_called_once()

        call_args = mock_user_repository.create.call_args[0][0]
        assert call_args.email == "test@example.com"
        assert call_args.username == "testuser"
        assert call_args.password == "hashed_password"
