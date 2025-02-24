import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    POSTGRES_DB: Final[str] = os.getenv('POSTGRES_DB', 'define me')
    POSTGRES_HOST: Final[str] = os.getenv('POSTGRES_HOST', 'define me')
    POSTGRES_USER: Final[str] = os.getenv('POSTGRES_USER', 'define me')
    POSTGRES_PASSWORD: Final[str] = os.getenv('POSTGRES_PASSWORD', 'define me')


class Constraints:
    POPUP_RUN_BOT: Final[str] = 'run bot'


class Config:
    TELEGRAM_TOKEN: Final[str] = os.getenv('TELEGRAM_TOKEN')
