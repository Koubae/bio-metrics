from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.application.account_service import AccountService
from src.account.infrastructure.account_repository import AccountRepositoryAdapter
from src.auth.infrastructure.access_token import HashLibPasswordHasher
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
) -> AccountRepositoryAdapter:
    repository = AccountRepositoryAdapter(session)
    return repository


async def provide_password_hasher() -> HashLibPasswordHasher:
    hasher = HashLibPasswordHasher()
    return hasher


async def get_account_service(
    repository: AccountRepositoryAdapter = Depends(get_account_repository),
    password_hasher: HashLibPasswordHasher = Depends(provide_password_hasher),
) -> AccountService:
    service = AccountService(repository, password_hasher)
    return service
