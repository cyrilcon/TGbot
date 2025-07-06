from types import TracebackType
from typing import Protocol

from domain.repositories.user_repo import UserRepository


class UnitOfWork(Protocol):
    user_repo: UserRepository

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
