import asyncio
import logging
import subprocess
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.handlers import main_router
from app.bot.middlewares import DbSessionMiddleware
from app.bot.middlewares.i18n import TranslatorRunnerMiddleware
from app.bot.service.commands import set_commands
from app.database.engine import engine
from app.loggers import configure_logging
from app.services.i18n import create_translator_hub
from app.shared.constraints import TelegramConfig


async def start_bot():
    """
    Configure and start telegram bot.
    """
    dp = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT
    )
    dp.include_routers(
        main_router,
    )
    session = async_sessionmaker(
        engine(),
        expire_on_commit=False,
    )

    dp.update.outer_middleware(DbSessionMiddleware(session))
    translator_hub: TranslatorHub = create_translator_hub()
    dp.update.middleware(TranslatorRunnerMiddleware())

    bot = Bot(
        token=TelegramConfig.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await set_commands(bot)
    try:
        await dp.start_polling(bot, _translator_hub=translator_hub)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    root = Path(__file__).parent.parent.parent
    subprocess.run(['alembic', 'upgrade', 'head'], cwd=root)
    configure_logging()
    asyncio.run(start_bot())
