from datetime import UTC, datetime

from sqlalchemy import insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User
from domain.repositories.user_repo import UserRepository
from infrastructure.db.models.users import users


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_social_id(self, social_id: int) -> User | None:
        stmt = select(users).where(users.c.social_id == social_id)
        result = await self.session.execute(stmt)
        row = result.fetchone()
        if row is None:
            return None
        return self._row_to_entity(row)

    async def add(self, user_entity: User) -> None:
        stmt = insert(users).values(
            social_id=user_entity.social_id,
            username=user_entity.username,
            registration_date=user_entity.registration_date or datetime.now(UTC),
            taps=user_entity.taps,
            name=user_entity.name,
            info=user_entity.info,
            photo=user_entity.photo,
        )
        await self.session.execute(stmt)

    async def update(self, user_entity: User) -> None:
        stmt = (
            update(users)
            .where(users.c.social_id == user_entity.social_id)
            .values(
                username=user_entity.username,
                registration_date=user_entity.registration_date or datetime.now(UTC),
                taps=user_entity.taps,
                name=user_entity.name,
                info=user_entity.info,
                photo=user_entity.photo,
            )
        )
        await self.session.execute(stmt)

    @staticmethod
    def _row_to_entity(row: Row) -> User:
        return User(
            id=row.id,
            social_id=row.social_id,
            username=row.username,
            registration_date=row.registration_date,
            taps=row.taps,
            name=row.name,
            info=row.info,
            photo=row.photo,
        )
