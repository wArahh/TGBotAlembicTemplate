import asyncio
import logging
from pathlib import Path

import requests
import subprocess
from logging.handlers import RotatingFileHandler

from app.bot.main import start_bot
from app.shared.constraints import TelegramConfig


class BaseFormatter(logging.Formatter):
    LEVEL_EMOJIS = {
        'DEBUG': '🐛',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '❗❗❗'
    }

    def get_emoji(self, levelname):
        self.emoji = self.LEVEL_EMOJIS.get(levelname)
        return self.emoji


class TelegramFormatter(BaseFormatter):
    def format(self, record):
        emoji = self.get_emoji(record.levelname)
        asctime = self.formatTime(record, self.datefmt if hasattr(self, 'datefmt') else None)
        formatted = (
            f'<b>{emoji} {record.levelname}</b> <code>[{asctime}]</code>\n'
            f'<b>Module:</b> <code>{record.name}</code>\n'
            f'<b>Function:</b> <code>{record.funcName}()</code>\n'
            f'<b>Location:</b> <code>{record.filename}:{record.lineno}</code>\n\n'
            f'{record.msg}'
        )
        return formatted


class ConsoleFormatter(BaseFormatter):
    def format(self, record):
        emoji = self.get_emoji(record.levelname)
        asctime = self.formatTime(record, self.datefmt if hasattr(self, 'datefmt') else None)

        try:
            message = record.msg % record.args if record.args else record.msg
        except (TypeError, ValueError):
            message = record.msg

        formatted = (
            f'{emoji} {record.levelname} - {record.name} - [{asctime}] - {record.funcName}() - {record.filename}:{record.lineno} - {message}'
        )
        return formatted


class TelegramLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        for chat_id in TelegramConfig.SEND_LOGS_CHAT_IDs:
            requests.post(
                url=f'https://api.telegram.org/bot{TelegramConfig.TELEGRAM_TOKEN}/sendMessage',
                json={
                    'chat_id': chat_id,
                    'text': log_entry,
                    'parse_mode': 'HTML',
                    'disable_web_page_preview': True
                }
            )


def configure_logging():
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / 'bot.log'
    log_file.touch(exist_ok=True)

    telegram_handler = TelegramLogHandler()
    telegram_handler.setLevel(logging.INFO)
    telegram_handler.setFormatter(TelegramFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ConsoleFormatter())

    general_logger = logging.getLogger()
    general_logger.setLevel(logging.INFO)
    general_logger.addHandler(console_handler)

    bot_logger = logging.getLogger('bot_logger')
    bot_handler = RotatingFileHandler(
        filename='logs/bot.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    bot_handler.setFormatter(ConsoleFormatter())
    bot_logger.addHandler(bot_handler)
    bot_logger.addHandler(telegram_handler)


async def run_project():
    subprocess.run(['alembic', 'upgrade', 'head'])
    configure_logging()
    await start_bot()


if __name__ == '__main__':
    asyncio.run(run_project())
