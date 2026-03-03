from uuid import UUID

from src.app.domain.entities.event_message import (
    EventUserData,
    PublishEventMessageInput,
)
from src.app.domain.entities.token import CreateTokenInput
from src.app.domain.entities.user import (
    CreateUserInput,
    CreateUserOutput,
    GetUserOutput,
    LoginInput,
    LoginOutput,
    UpdateUserInput,
    UpdateUserOutput,
)
from src.app.domain.ports import (
    EventPublisherPort,
    TokenProviderPort,
    UserRepositoryPort,
)


class AuthService:
    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
        token_provider_port: TokenProviderPort,
        event_publisher_port: EventPublisherPort,
    ):
        self._user_repository_port = user_repository_port
        self._token_provider_port = token_provider_port
        self._event_publisher_port = event_publisher_port

    async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
        existing_user = await self._user_repository_port.get_by_email(input_data.email)
        if existing_user:
            return CreateUserOutput(
                user=None, success=False, message="Email already registered"
            )

        existing_user = await self._user_repository_port.get_by_username(
            input_data.username
        )
        if existing_user:
            return CreateUserOutput(
                user=None, success=False, message="Username already taken"
            )

        user_entity = await self._user_repository_port.create(input_data)

        event_message = PublishEventMessageInput(
            event_name="user.created",
            data=EventUserData(
                user_id=str(user_entity.id),
                email=user_entity.email,
                username=user_entity.username,
            ),
        )
        await self._event_publisher_port.publish(event_message)

        return CreateUserOutput(
            user=user_entity, success=True, message="User created successfully"
        )

    async def login(self, input_data: LoginInput) -> LoginOutput:
        user = await self._user_repository_port.get_by_email(input_data.email)
        if not user:
            raise ValueError("Invalid credentials")

        token_input = CreateTokenInput(user_id=str(user.id), email=user.email)

        access_token_output = self._token_provider_port.create_access_token(token_input)
        refresh_token_output = self._token_provider_port.create_refresh_token(
            token_input
        )

        event_message = PublishEventMessageInput(
            event_name="user.login",
            data=EventUserData(
                user_id=str(user.id),
                email=user.email,
                username=user.username,
            ),
        )
        await self._event_publisher_port.publish(event_message)

        return LoginOutput(
            access_token=access_token_output.access_token,
            refresh_token=refresh_token_output.refresh_token,
            token_type="bearer",
            user=user,
        )

    async def get_user(self, user_id: UUID) -> GetUserOutput:
        user = await self._user_repository_port.get_by_id(user_id)
        if not user:
            return GetUserOutput(user=None, success=False, message="User not found")
        return GetUserOutput(user=user, success=True)

    async def get_user_by_email(self, email: str) -> GetUserOutput:
        user = await self._user_repository_port.get_by_email(email)
        if not user:
            return GetUserOutput(user=None, success=False, message="User not found")
        return GetUserOutput(user=user, success=True)

    async def update_user(self, input_data: UpdateUserInput) -> UpdateUserOutput:
        existing_user = await self._user_repository_port.get_by_id(input_data.id)
        if not existing_user:
            return UpdateUserOutput(user=None, success=False, message="User not found")

        if input_data.email and input_data.email != existing_user.email:
            email_user = await self._user_repository_port.get_by_email(input_data.email)
            if email_user:
                return UpdateUserOutput(
                    user=None, success=False, message="Email already registered"
                )
            existing_user.email = input_data.email

        if input_data.username and input_data.username != existing_user.username:
            username_user = await self._user_repository_port.get_by_username(
                input_data.username
            )
            if username_user:
                return UpdateUserOutput(
                    user=None, success=False, message="Username already taken"
                )
            existing_user.username = input_data.username

        if input_data.is_active is not None:
            existing_user.is_active = input_data.is_active

        if input_data.is_admin is not None:
            existing_user.is_admin = input_data.is_admin

        updated_user = await self._user_repository_port.update(existing_user)

        event_message = PublishEventMessageInput(
            event_name="user.updated",
            data=EventUserData(
                user_id=str(updated_user.id),
                email=updated_user.email,
                username=updated_user.username,
            ),
        )
        await self._event_publisher_port.publish(event_message)

        return UpdateUserOutput(
            user=updated_user, success=True, message="User updated successfully"
        )
