from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Admin


async def check_user_admin(
        session: AsyncSession,
        telegram_id: int
) -> bool:
    """
    :param session: async session.
    :param telegram_id: telegram id of user.

    :return: True if admin, else False.
    """
    statement = select(Admin).where(Admin.telegram_id == telegram_id)

    return (await session.execute(statement)).scalar_one_or_none() is not None
