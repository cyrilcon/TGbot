from types import TracebackType
from typing import Protocol

from domain.repositories import AbstractUserRepository


class AbstractUnitOfWork(Protocol):
    user_repo: AbstractUserRepository

    async def __aenter__(self) -> "AbstractUnitOfWork":
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
