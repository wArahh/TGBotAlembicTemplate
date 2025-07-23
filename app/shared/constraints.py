import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class TelegramConfig:
    TELEGRAM_TOKEN: Final[str] = os.getenv('TELEGRAM_TOKEN')
    ADMIN_CHAT_ID: Final[str] = os.getenv('ADMIN_CHAT_ID')
    SEND_LOGS_CHAT_IDs = [ADMIN_CHAT_ID]


class PostgresConfig:
    POSTGRES_DB: Final[str] = os.getenv('POSTGRES_DB')
    POSTGRES_HOST: Final[str] = os.getenv('POSTGRES_HOST')
    POSTGRES_USER: Final[str] = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: Final[str] = os.getenv('POSTGRES_PASSWORD')


class Constraints:
    POPUP_RUN_BOT: Final[str] = 'run bot'
