from uuid import UUID

from src.app.domain.entities.event_message import EventMessage
from src.app.domain.entities.token import CreateTokenInput
from src.app.domain.entities.user import (
    CreateUserInput,
    CreateUserOutput,
    LoginInput,
    LoginOutput,
    UpdateUserInput,
    UserEntity,
)
from src.app.domain.ports import (
    EventPublisherPort,
    TokenProviderPort,
    UserRepositoryPort,
)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        token_provider: TokenProviderPort,
        event_publisher: EventPublisherPort,
    ):
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.event_publisher = event_publisher

    async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
        existing_user = await self.user_repository.get_by_email(input_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        existing_user = await self.user_repository.get_by_username(input_data.username)
        if existing_user:
            raise ValueError("Username already taken")

        user_entity = await self.user_repository.create(input_data)

        event_message = EventMessage(
            event_name="user.created",
            data={
                "user_id": str(user_entity.id),
                "email": user_entity.email,
                "username": user_entity.username,
            },
        )
        await self.event_publisher.publish(event_message)

        return CreateUserOutput(
            id=user_entity.id,
            email=user_entity.email,
            username=user_entity.username,
            is_active=user_entity.is_active,
            is_admin=user_entity.is_admin,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
        )

    async def login(self, input_data: LoginInput) -> LoginOutput:
        user = await self.user_repository.get_by_email(input_data.email)
        if not user:
            raise ValueError("Invalid credentials")

        token_input = CreateTokenInput(user_id=str(user.id), email=user.email)

        access_token_output = self.token_provider.create_access_token(token_input)
        refresh_token_output = self.token_provider.create_refresh_token(token_input)

        event_message = EventMessage(
            event_name="user.login",
            data={
                "user_id": str(user.id),
                "email": user.email,
            },
        )
        await self.event_publisher.publish(event_message)

        return LoginOutput(
            access_token=access_token_output.access_token,
            refresh_token=refresh_token_output.refresh_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            username=user.username,
        )

    async def get_user_by_id(self, user_id: UUID) -> UserEntity:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> UserEntity:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        return user

    async def update_user(
        self, user_id: UUID, input_data: UpdateUserInput
    ) -> UserEntity:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")

        if input_data.email and input_data.email != existing_user.email:
            email_user = await self.user_repository.get_by_email(input_data.email)
            if email_user:
                raise ValueError("Email already registered")
            existing_user.email = input_data.email

        if input_data.username and input_data.username != existing_user.username:
            username_user = await self.user_repository.get_by_username(
                input_data.username
            )
            if username_user:
                raise ValueError("Username already taken")
            existing_user.username = input_data.username

        if input_data.is_active is not None:
            existing_user.is_active = input_data.is_active

        if input_data.is_admin is not None:
            existing_user.is_admin = input_data.is_admin

        updated_user = await self.user_repository.update(existing_user)

        event_message = EventMessage(
            event_name="user.updated",
            data={
                "user_id": str(updated_user.id),
                "email": updated_user.email,
                "username": updated_user.username,
            },
        )
        await self.event_publisher.publish(event_message)

        return updated_user
