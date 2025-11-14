import os

from dotenv import load_dotenv

load_dotenv()


class TelegramConfig:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    SEND_LOGS_CHAT_IDs = [ADMIN_CHAT_ID]


class PostgresConfig:
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


class Config:
    DEBUG = os.getenv('DEBUG', '0') == '1'
