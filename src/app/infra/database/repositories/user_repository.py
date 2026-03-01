from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select

from src.app.infra.database.repositories.models import UserDB


@dataclass
class InfraCreateUserInput:
    email: str
    username: str
    password: str


@dataclass
class InfraUserEntity:
    id: UUID
    email: str
    username: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_email(self, email: str) -> Optional[InfraUserEntity]:
        async with self.session_factory() as session:
            result = await session.execute(select(UserDB).where(UserDB.email == email))
            user_db = result.scalar_one_or_none()
            if user_db:
                return self._db_to_entity(user_db)
            return None

    async def get_by_username(self, username: str) -> Optional[InfraUserEntity]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserDB).where(UserDB.username == username)
            )
            user_db = result.scalar_one_or_none()
            if user_db:
                return self._db_to_entity(user_db)
            return None

    async def get_by_id(self, user_id: UUID) -> Optional[InfraUserEntity]:
        async with self.session_factory() as session:
            result = await session.execute(select(UserDB).where(UserDB.id == user_id))
            user_db = result.scalar_one_or_none()
            if user_db:
                return self._db_to_entity(user_db)
            return None

    async def create(self, input_data: InfraCreateUserInput) -> InfraUserEntity:
        async with self.session_factory() as session:
            user_db = UserDB(
                id=uuid4(),
                email=input_data.email,
                username=input_data.username,
                hashed_password=input_data.password,
                is_active=True,
                is_admin=False,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )

            session.add(user_db)
            await session.commit()
            await session.refresh(user_db)

            return self._db_to_entity(user_db)

    async def update(self, user: InfraUserEntity) -> InfraUserEntity:
        async with self.session_factory() as session:
            result = await session.execute(select(UserDB).where(UserDB.id == user.id))
            user_db = result.scalar_one_or_none()
            if not user_db:
                raise ValueError("User not found")

            user_db.email = user.email
            user_db.username = user.username
            user_db.is_active = user.is_active
            user_db.is_admin = user.is_admin
            user_db.updated_at = datetime.now(timezone.utc)

            await session.commit()
            await session.refresh(user_db)

            return self._db_to_entity(user_db)

    async def delete(self, user_id: UUID) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(UserDB).where(UserDB.id == user_id))
            user_db = result.scalar_one_or_none()
            if not user_db:
                return False

            await session.delete(user_db)
            await session.commit()
            return True

    def _db_to_entity(self, user_db: UserDB) -> InfraUserEntity:
        return InfraUserEntity(
            id=user_db.id,
            email=user_db.email,
            username=user_db.username,
            hashed_password=user_db.hashed_password,
            is_active=user_db.is_active,
            is_admin=user_db.is_admin,
            created_at=user_db.created_at,
            updated_at=user_db.updated_at,
        )
