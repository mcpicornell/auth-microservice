import pytest

# pylint: disable=protected-access
from src.app.dependencies_container import DependenciesContainer


class TestDependenciesContainer:
    @pytest.fixture
    def mock_settings(self, mocker):
        settings = mocker.Mock()
        settings.DB_SQL_URL = "postgresql://test"
        settings.DB_SQL_ECHO = False
        settings.RABBITMQ_HOST = "localhost"
        settings.RABBITMQ_PORT = 5672
        settings.RABBITMQ_USER = "guest"
        settings.RABBITMQ_PASSWORD = "guest"
        settings.RABBITMQ_VHOST = "/"
        settings.JWT_SECRET_KEY = "test_secret"
        settings.JWT_ALGORITHM = "HS256"
        settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
        settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
        mocker.patch(
            "src.app.dependencies_container.get_settings", return_value=settings
        )
        return settings

    @pytest.fixture
    def container(self):
        return DependenciesContainer()

    @pytest.mark.asyncio
    async def test_initialize_adapters(self, container, mocker):

        mock_user_repository = mocker.patch(
            "src.app.dependencies_container.UserRepository"
        )
        mock_password_adapter = mocker.patch(
            "src.app.dependencies_container.PasswordAdapter"
        )
        mock_user_adapter = mocker.patch("src.app.dependencies_container.UserAdapter")
        mock_jwt_adapter = mocker.patch("src.app.dependencies_container.JWTAdapter")
        mock_rabbitmq_adapter = mocker.patch(
            "src.app.dependencies_container.RabbitMQAdapter"
        )

        container._db_session_factory = mocker.Mock()
        container._rabbitmq_manager = mocker.Mock()
        container._jwt_manager = mocker.Mock()

        mock_rabbitmq_adapter_instance = mocker.Mock()
        mock_rabbitmq_adapter_instance.connect = mocker.AsyncMock()
        mock_rabbitmq_adapter.return_value = mock_rabbitmq_adapter_instance

        await container._initialize_managers()
        await container._initialize_adapters()

        mock_user_repository.assert_called_once_with(container._db_session_factory)
        mock_password_adapter.assert_called_once()
        mock_user_adapter.assert_called_once()
        mock_jwt_adapter.assert_called_once_with(container._jwt_manager)
        mock_rabbitmq_adapter.assert_called_once_with(container._rabbitmq_manager)
        mock_rabbitmq_adapter_instance.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialize_services(self, container, mocker):

        container._db_session_factory = mocker.Mock()
        container._rabbitmq_manager = mocker.Mock()
        container._jwt_manager = mocker.Mock()

        mock_rabbitmq_adapter_instance = mocker.Mock()
        mock_rabbitmq_adapter_instance.connect = mocker.AsyncMock()
        container._rabbitmq_adapter = mock_rabbitmq_adapter_instance
        container._jwt_adapter = mocker.Mock()
        container._user_adapter = mocker.Mock()
        container._password_adapter = mocker.Mock()
        container._user_repository = mocker.Mock()

        await container._initialize_managers()
        await container._initialize_adapters()
        await container._initialize_services()
        await container._initialize_handlers()

    @pytest.mark.asyncio
    async def test_full_initialization(self, mock_settings, mocker):
        container = DependenciesContainer()

        mock_rabbitmq_adapter = mocker.patch(
            "src.app.dependencies_container.RabbitMQAdapter"
        )

        mock_session_factory = mocker.Mock()
        container._db_session_factory = mock_session_factory
        container._rabbitmq_manager = mocker.Mock()
        container._jwt_manager = mocker.Mock()

        mock_rabbitmq_adapter_instance = mocker.Mock()
        mock_rabbitmq_adapter_instance.connect = mocker.AsyncMock()
        mock_rabbitmq_adapter.return_value = mock_rabbitmq_adapter_instance

        await container.initialize()

        assert container._rabbitmq_manager is not None
        assert container._jwt_manager is not None
        assert container._jwt_adapter is not None
        assert container._rabbitmq_adapter is not None
        assert container._auth_service is not None
        assert container._auth_handler is not None
        assert container._user_handler is not None

        mock_rabbitmq_adapter_instance.connect.assert_called_once()

    def test_getters(self, container, mocker):

        container._user_adapter = mocker.Mock()
        container._jwt_adapter = mocker.Mock()
        container._rabbitmq_adapter = mocker.Mock()
        container._auth_service = mocker.Mock()
        container._auth_handler = mocker.Mock()
        container._user_handler = mocker.Mock()

        assert container.get_user_adapter() is container._user_adapter
        assert container.get_jwt_adapter() is container._jwt_adapter
        assert container.get_rabbitmq_adapter() is container._rabbitmq_adapter
        assert container.get_auth_service() is container._auth_service
        assert container.get_auth_handler() is container._auth_handler
        assert container.get_user_handler() is container._user_handler

    @pytest.mark.asyncio
    async def test_cleanup(self, mock_settings, mocker):
        container = DependenciesContainer()

        container._db_engine = mocker.Mock()
        container._db_engine.dispose = mocker.AsyncMock()
        container._rabbitmq_adapter = mocker.Mock()
        container._rabbitmq_adapter.disconnect = mocker.AsyncMock()

        await container.close()

        container._db_engine.dispose.assert_called_once()
        container._rabbitmq_adapter.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_db_session(self, mock_settings, mocker):
        container = DependenciesContainer()
        mock_session = mocker.Mock()
        mock_session_factory = mocker.Mock(return_value=mock_session)
        container._db_session_factory = mock_session_factory

        session = container.get_db_session()

        mock_session_factory.assert_called_once()
        assert session is mock_session

    def test_initialization_state(self, mock_settings):
        container = DependenciesContainer()

        assert container._db_engine is None
        assert container._db_session_factory is None
        assert container._user_repository is None
        assert container._password_adapter is None
        assert container._user_adapter is None
        assert container._rabbitmq_manager is None
        assert container._jwt_manager is None
        assert container._jwt_adapter is None
        assert container._rabbitmq_adapter is None
        assert container._auth_service is None
        assert container._auth_handler is None
        assert container._user_handler is None
