from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.shared.constraints import Constraints


async def set_commands(bot: Bot):
    """
    set bot commands in popup menu.

    :param bot: telegram bot.
    :return: set of bot commands in popup menu.
    """
    commands = [
        BotCommand(
            command='start',
            description=Constraints.POPUP_RUN_BOT,
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
