import asyncio
import subprocess

from app.bot.main import start_bot
from app.loggers import configure_logging


async def run_all():
    subprocess.run(['alembic', 'upgrade', 'head'])
    configure_logging()
    await start_bot()


if __name__ == '__main__':
    asyncio.run(run_all())
