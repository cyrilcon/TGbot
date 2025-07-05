from aiogram import Bot, types


async def set_default_commands(bot: Bot, admins: list[int]) -> None:
    """
    Set bot commands

    :param bot: Bot instance.
    :param admins: List of admin user IDs.
    """

    commands = [
        types.BotCommand(command="help", description="ℹ️ Info"),
        types.BotCommand(command="start", description="🔄 Restart"),
    ]
    await bot.set_my_commands(commands)

    admin_commands = [
        *commands,
        types.BotCommand(command="admin", description="📊 Admin commands"),
    ]
    for admin in admins:
        scope = types.BotCommandScopeChat(chat_id=admin)
        await bot.set_my_commands(admin_commands, scope=scope)
