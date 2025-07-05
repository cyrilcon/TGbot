from aiogram import Router

from .admin import admin_routers
from .unprocessed_messages import unprocessed_messages_router
from .user import user_routers

routers = Router()
routers.include_routers(
    admin_routers,
    user_routers,
    unprocessed_messages_router,  # Must be the latest
)

__all__ = ("routers",)
