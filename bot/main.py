import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.main import engine
from bot.handlers import main_router
from bot.service.config import Config
from bot.service.commands import set_commands
from bot.middlewares import DbSessionMiddleware

logging.basicConfig(
    format='%(levelname)s %(filename)s:%(lineno)d '
           '[%(asctime)s] - %(name)s - %(message)s',
    level=logging.INFO
)

logs = logging.getLogger(__name__)


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

    bot = Bot(
        token=Config.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(e)
