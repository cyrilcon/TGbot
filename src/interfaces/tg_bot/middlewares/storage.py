from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject


class StorageMiddleware(BaseMiddleware):
    """
    Middleware to retrieve storage.
    """

    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["storage"] = self.storage
        return await handler(event, data)
