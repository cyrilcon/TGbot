from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import Config


class AdminFilter(BaseFilter):
    """
    Filter for verifying the authenticity of the administrator.
    """

    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
