from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]),
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Middleware for automatically adding an asynchronous SQLAlchemy session
        to aiogram handlers.

        A new session is created for each update and injected into `data['session']`.
        The session is automatically closed after the handler is executed.

        Example handler with session access:
            async def handler(message: Message, session: AsyncSession):
                result = await session.execute(select(User).where(User.id == 1))
        """
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
