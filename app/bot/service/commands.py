from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from fluentogram import TranslatorHub


async def set_commands(
        bot: Bot,
        translator_hub: TranslatorHub
):
    """
    set bot commands in popup menu.
    """
    i18n = translator_hub.get_translator_by_locale(locale='en')
    commands = [
        BotCommand(
            command='start',
            description=i18n.popup.run_bot(),
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
