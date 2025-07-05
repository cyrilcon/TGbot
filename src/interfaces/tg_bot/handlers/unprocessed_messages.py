from aiogram import Router
from aiogram.types import Message

unprocessed_messages_router = Router()


@unprocessed_messages_router.message()
async def unprocessed_messages(message: Message) -> None:
    """
    Processing of unprocessed messages.

    :param message: Incoming message from the user.
    """

    await message.answer("I didn't understand you 😕\nCommand list – /help")
