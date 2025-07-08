

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.account.infrastructure.models import Account
from src.auth.domain.entities import Role


async def create_account(db: AsyncSession, username: str, password: str, role: Role):
    user = Account(username=username, password=password, role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_account_by_username(db: AsyncSession, username: str):
    stmt = select(Account).where(Account.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()
