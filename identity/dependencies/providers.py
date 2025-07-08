from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.application.account_service import AccountService
from src.account.infrastructure.account_repository import AccountRepositoryAdapter
from src.auth.application.auth_service import AuthService
from src.auth.infrastructure.access_token import (
    HashLibPasswordHasher,
    JWTAccessTokenAuth,
)
from src.core.infrastructure.database.sqlalchemy_db import SQLAlchemyDatabase


def get_database() -> SQLAlchemyDatabase:
    database = SQLAlchemyDatabase.get()
    return database


async def provide_session(
    database: SQLAlchemyDatabase = Depends(get_database),
) -> AsyncGenerator[AsyncSession, Any]:
    async with database.get_session() as session:
        yield session


async def provide_account_repository(
    session: AsyncSession = Depends(provide_session),
) -> AccountRepositoryAdapter:
    repository = AccountRepositoryAdapter(session)
    return repository


async def provide_password_hasher() -> HashLibPasswordHasher:
    hasher = HashLibPasswordHasher()
    return hasher


async def provide_access_token_generator() -> JWTAccessTokenAuth:
    auth = JWTAccessTokenAuth()
    return auth


async def provide_account_service(
    repository: AccountRepositoryAdapter = Depends(provide_account_repository),
    password_hasher: HashLibPasswordHasher = Depends(provide_password_hasher),
) -> AccountService:
    service = AccountService(repository, password_hasher)
    return service


async def provide_auth_service(
    password_hasher: HashLibPasswordHasher = Depends(provide_password_hasher),
    auth: JWTAccessTokenAuth = Depends(provide_access_token_generator),
    auth_service: AccountService = Depends(provide_account_service),
) -> AuthService:
    service = AuthService(password_hasher, auth, auth_service)
    return service
