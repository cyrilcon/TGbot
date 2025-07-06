from typing import Protocol

from domain.entities import User


class AbstractUserRepository(Protocol):
    async def get_by_social_id(self, social_id: int) -> User | None:
        pass

    async def add(self, user: User) -> None:
        pass

    async def update(self, user: User) -> None:
        pass
