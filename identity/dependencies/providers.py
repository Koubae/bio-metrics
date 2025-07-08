from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.infrastructure.account_repository import AccountRepository
from src.core.infrastructure.database.sqlalchemy_db import SQLAlchemyDatabase


def get_database() -> SQLAlchemyDatabase:
    database = SQLAlchemyDatabase.get()
    return database


async def get_session(
    database: SQLAlchemyDatabase = Depends(get_database),
) -> AsyncGenerator[AsyncSession, Any]:
    async with database.get_session() as session:
        yield session


async def get_account_repository(
    session: AsyncSession = Depends(get_session),
) -> AccountRepository:
    repository = AccountRepository(session)
    return repository
