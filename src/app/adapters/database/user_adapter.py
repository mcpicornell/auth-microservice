from typing import Any, Dict, Optional, Protocol
from uuid import UUID

from src.app.domain.entities.user import CreateUserInput, UserEntity
from src.app.domain.ports.password_hasher_port import PasswordHasherPort
from src.app.infra.database.repositories.user_repository import (
    InfraCreateUserInput,
    InfraUserEntity,
    UserRepository,
)


class UserAdapterPort(Protocol):
    async def get_by_email(self, email: str) -> Optional[UserEntity]: ...
    async def get_by_username(self, username: str) -> Optional[UserEntity]: ...
    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]: ...
    async def create(self, input_data: CreateUserInput) -> UserEntity: ...
    async def update(self, user: UserEntity) -> UserEntity: ...
    async def delete(self, user_id: UUID) -> bool: ...
    def entity_to_dict(self, entity: UserEntity) -> Dict[str, Any]: ...


class UserAdapter(UserAdapterPort):
    def __init__(
        self, user_repository: UserRepository, password_hasher: PasswordHasherPort
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        infra_user = await self.user_repository.get_by_email(email)
        return self._infra_to_domain(infra_user) if infra_user else None

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        infra_user = await self.user_repository.get_by_username(username)
        return self._infra_to_domain(infra_user) if infra_user else None

    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        infra_user = await self.user_repository.get_by_id(user_id)
        return self._infra_to_domain(infra_user) if infra_user else None

    async def create(self, input_data: CreateUserInput) -> UserEntity:
        hashed_password = self.password_hasher.hash_password(input_data.password)

        infra_input = InfraCreateUserInput(
            email=input_data.email,
            username=input_data.username,
            password=hashed_password,
        )

        infra_user = await self.user_repository.create(infra_input)
        return self._infra_to_domain(infra_user)

    async def update(self, user: UserEntity) -> UserEntity:
        infra_user = self._domain_to_infra(user)
        updated_infra_user = await self.user_repository.update(infra_user)
        return self._infra_to_domain(updated_infra_user)

    async def delete(self, user_id: UUID) -> bool:
        return await self.user_repository.delete(user_id)

    def entity_to_dict(self, entity: UserEntity) -> Dict[str, Any]:
        return {
            "id": entity.id,
            "email": entity.email,
            "username": entity.username,
            "is_active": entity.is_active,
            "is_admin": entity.is_admin,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }

    def _infra_to_domain(self, infra_user: InfraUserEntity) -> UserEntity:
        return UserEntity(
            id=infra_user.id,
            email=infra_user.email,
            username=infra_user.username,
            hashed_password=infra_user.hashed_password,
            is_active=infra_user.is_active,
            is_admin=infra_user.is_admin,
            created_at=infra_user.created_at,
            updated_at=infra_user.updated_at,
        )

    def _domain_to_infra(self, domain_user: UserEntity) -> InfraUserEntity:
        return InfraUserEntity(
            id=domain_user.id,
            email=domain_user.email,
            username=domain_user.username,
            hashed_password=domain_user.hashed_password,
            is_active=domain_user.is_active,
            is_admin=domain_user.is_admin,
            created_at=domain_user.created_at,
            updated_at=domain_user.updated_at,
        )
