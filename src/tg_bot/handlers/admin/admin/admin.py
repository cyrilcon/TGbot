from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin(message: Message) -> None:
    """
    Process the /admin command.

    :param message: Incoming message from the user.
    """

    await message.answer("Hello, admin!!")
