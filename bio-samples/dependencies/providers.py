from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.access_token import JWTAccessTokenAuth
from src.core.infrastructure.database.sqlalchemy_db import SQLAlchemyDatabase
from src.sample.application.sample_service import SampleService
from src.sample.infrastructure.sample_repository import SampleRepositoryAdapter


def get_database() -> SQLAlchemyDatabase:
    database = SQLAlchemyDatabase.get()
    return database


async def provide_session(
    database: SQLAlchemyDatabase = Depends(get_database),
) -> AsyncGenerator[AsyncSession, Any]:
    async with database.get_session() as session:
        yield session


async def provide_access_token_auth() -> JWTAccessTokenAuth:
    auth = JWTAccessTokenAuth()
    return auth


async def provide_sample_repository(
    session: AsyncSession = Depends(provide_session),
) -> SampleRepositoryAdapter:
    repository = SampleRepositoryAdapter(session)
    return repository


async def provide_sample_service(
    repository: SampleRepositoryAdapter = Depends(provide_sample_repository),
) -> SampleService:
    service = SampleService(repository)
    return service
