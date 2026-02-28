from typing import Optional
from uuid import UUID

from src.app.domain.entities.user import CreateUserInput, UserEntity
from src.app.domain.ports.password_hasher_port import PasswordHasherPort
from src.app.domain.ports.user_repository_port import UserRepositoryPort
from src.app.infra.database.repositories.user_repository import UserRepository


class UserAdapter(UserRepositoryPort):
    def __init__(
        self, user_repository: UserRepository, password_hasher: PasswordHasherPort
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        return await self.user_repository.get_by_email(email)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        return await self.user_repository.get_by_username(username)

    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        return await self.user_repository.get_by_id(user_id)

    async def create(self, input_data: CreateUserInput) -> UserEntity:
        hashed_password = self.password_hasher.hash_password(input_data.password)

        create_input = CreateUserInput(
            email=input_data.email,
            username=input_data.username,
            password=hashed_password,
        )

        return await self.user_repository.create(create_input)

    async def update(self, user: UserEntity) -> UserEntity:
        return await self.user_repository.update(user)

    async def delete(self, user_id: UUID) -> bool:
        return await self.user_repository.delete(user_id)
