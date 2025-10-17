from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.bot import bot_logger

main_router = Router()


@main_router.message(Command('start'))
async def welcome_message(
        message: Message,
        i18n: TranslatorRunner
):
    """
    send welcome message.
    """
    bot_logger.info(i18n.logs.bot.bot_logger_works())
    await message.answer(i18n.user.message.welcome_message())
