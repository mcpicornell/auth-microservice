from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.adapters.auth_adapter import AuthAdapter
from src.app.adapters.database.user_adapter import UserAdapter
from src.app.adapters.messaging.rabbitmq_adapter import RabbitMQAdapter
from src.app.adapters.security.jwt_adapter import JWTAdapter
from src.app.adapters.security.password_adapter import PasswordAdapter
from src.app.domain.services.auth_service import AuthService
from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter
from src.app.infra.api.handlers.auth_handler import AuthHandler
from src.app.infra.api.handlers.user_handler import UserHandler
from src.app.infra.auth.jwt_manager import JWTManager
from src.app.infra.database.repositories.user_repository import UserRepository
from src.app.infra.messaging.rabbitmq_manager import RabbitMQManager
from src.app.settings import get_settings


class DependenciesContainer:
    def __init__(self):
        self.settings = get_settings()
        self._db_engine = None
        self._db_session_factory = None
        self._user_repository = None
        self._user_adapter = None
        self._password_adapter = None
        self._jwt_adapter = None
        self._rabbitmq_adapter = None
        self._rabbitmq_manager = None
        self._jwt_manager = None
        self._auth_service = None
        self._user_service_adapter = None
        self._auth_handler = None
        self._user_handler = None

    async def initialize(self):
        await self._initialize_database()
        await self._initialize_managers()
        await self._initialize_adapters()
        await self._initialize_services()
        await self._initialize_infra_adapters()
        await self._initialize_handlers()

    async def _initialize_database(self):
        db_url = self.settings.DB_SQL_URL.replace(
            "postgresql://", "postgresql+asyncpg://"
        )
        self._db_engine = create_async_engine(db_url, echo=self.settings.DB_SQL_ECHO)
        self._db_session_factory = sessionmaker(
            self._db_engine, class_=AsyncSession, expire_on_commit=False
        )

    async def _initialize_managers(self):
        self._rabbitmq_manager = RabbitMQManager(
            host=self.settings.RABBITMQ_HOST,
            port=self.settings.RABBITMQ_PORT,
            user=self.settings.RABBITMQ_USER,
            password=self.settings.RABBITMQ_PASSWORD,
            vhost=self.settings.RABBITMQ_VHOST,
        )

        self._jwt_manager = JWTManager(
            secret_key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM,
            access_expire_minutes=self.settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_expire_days=self.settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        )

    async def _initialize_adapters(self):
        self._user_repository = UserRepository(self._db_session_factory)
        self._user_adapter = UserAdapter(self._user_repository, self._password_adapter)
        self._password_adapter = PasswordAdapter()
        self._jwt_adapter = JWTAdapter(self._jwt_manager)
        self._rabbitmq_adapter = RabbitMQAdapter(self._rabbitmq_manager)
        await self._rabbitmq_adapter.connect()

    async def _initialize_services(self):
        self._auth_service = AuthService(
            user_repository=self._user_adapter,
            token_provider=self._jwt_adapter,
            event_publisher=self._rabbitmq_adapter,
        )

    async def _initialize_infra_adapters(self):
        auth_adapter = AuthAdapter(
            auth_service=self._auth_service,
            entity_mapper=self._user_adapter,
        )
        self._user_service_adapter = UserServiceAdapter(
            auth_service=auth_adapter,
        )

    async def _initialize_handlers(self):
        self._auth_handler = AuthHandler(self._user_service_adapter)
        self._user_handler = UserHandler(self._user_service_adapter)

    def get_db_session(self) -> AsyncSession:
        return self._db_session_factory()

    def get_user_adapter(self) -> UserAdapter:
        return self._user_adapter

    def get_jwt_adapter(self) -> JWTAdapter:
        return self._jwt_adapter

    def get_rabbitmq_adapter(self) -> RabbitMQAdapter:
        return self._rabbitmq_adapter

    def get_auth_service(self) -> AuthService:
        return self._auth_service

    def get_auth_handler(self) -> AuthHandler:
        return self._auth_handler

    def get_user_handler(self) -> UserHandler:
        return self._user_handler

    async def close(self):
        if self._db_engine:
            await self._db_engine.dispose()
        if self._rabbitmq_adapter:
            await self._rabbitmq_adapter.disconnect()
