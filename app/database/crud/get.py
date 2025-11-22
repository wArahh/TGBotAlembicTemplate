from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Admin


async def check_user_admin(
        telegram_id: int,
        session: AsyncSession,
) -> bool:
    """
    :param session: async session.
    :param telegram_id: telegram id of user.

    :return: True if admin, else False.
    """
    statement = select(
        exists()
    ).where(
        Admin.telegram_id == telegram_id
    )
    result = await session.execute(statement)
    return result.scalar()
