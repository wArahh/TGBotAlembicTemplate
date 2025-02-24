from sqlalchemy.ext.asyncio import create_async_engine
from bot.service.config import PostgresConfig


DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{PostgresConfig.POSTGRES_USER}:'
    f'{PostgresConfig.POSTGRES_PASSWORD}'
    f'@{PostgresConfig.POSTGRES_HOST}/{PostgresConfig.POSTGRES_DB}'
)


def engine():
    return create_async_engine(DATABASE_URL)
