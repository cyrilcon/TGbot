from types import TracebackType
from typing import Protocol

from domain.repositories import UserRepository


class UnitOfWork(Protocol):
    user_repo: UserRepository

    async def __aenter__(self) -> "UnitOfWork":
        pass

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
