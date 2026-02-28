from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.app.domain.entities.user import UserEntity, CreateUserInput


class UserRepositoryPort(ABC):
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def create(self, input_data: CreateUserInput) -> UserEntity:
        pass
    
    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        pass
