import asyncio
import contextlib
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import AiogramError
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from config import config

from .handlers import routers
from .middlewares import ConfigMiddleware, StorageMiddleware
from .services import set_default_commands


async def on_startup(bot: Bot) -> None:
    """
    Called on bot startup.
    """

    # # Reboot scheduler after bot restart
    # await restart_scheduler(bot)

    # Set bot commands
    admins = config.tg_bot.admin_ids

    await set_default_commands(bot, admins)

    # Send start message to admins
    for admin in admins:
        with contextlib.suppress(AiogramError):
            await bot.send_message(chat_id=admin, text="Bot restarted!!")


async def on_shutdown() -> None:
    """
    Called on bot shutdown.
    """


def register_global_middlewares(dp: Dispatcher, storage: RedisStorage) -> None:
    """
    Register global middlewares for the given dispatcher.

    :param dp: The dispatcher instance.
    :param storage: Storage for FSM.
    """

    middleware_types = [
        ConfigMiddleware(config),
        StorageMiddleware(storage),
    ]

    for middleware_type in middleware_types:
        dp.message.middleware(middleware_type)
        dp.callback_query.middleware(middleware_type)


def setup_logging() -> None:
    """
    Set up logging configuration for the application.
    """

    logging_level = config.logging_level
    bl.basic_colorized_config(level=logging_level)

    logging.basicConfig(
        level=logging_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting the bot")


def get_storage() -> RedisStorage:
    """
    Return storage based on the provided configuration.

    Returns:
        Storage: The storage object based on the configuration.
    """

    return RedisStorage.from_url(
        config.redis.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )


# async def restart_scheduler(bot: Bot):
#     """
#     The scheduler is restored after the bot is restarted.
#     :param bot: Bot instance.
#     """
#
#     # Reboot scheduler after bot restart
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(
#         saturday_post,
#         trigger=CronTrigger(
#             day_of_week="sat",
#             hour=9,
#             minute=0,
#             timezone=config.timezone,
#         ),
#         args=[bot],
#     )
#     # Start the scheduler
#     scheduler.start()


async def main() -> None:
    # Set logging
    setup_logging()

    storage = get_storage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.CHAT,  # CHAT - state and data common for the whole chat
    )

    # Installing routers
    dp.include_routers(routers)

    # Installing middlewares
    register_global_middlewares(dp, storage)

    await on_startup(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.exception("Stopping the bot")
