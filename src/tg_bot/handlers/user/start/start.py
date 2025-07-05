from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message) -> None:
    """
    Process the /start command.

    :param message: Incoming message from the user.
    """

    await message.answer("Hello, user!!")
