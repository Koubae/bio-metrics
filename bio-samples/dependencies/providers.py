from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.access_token import JWTAccessTokenAuth
from src.core.infrastructure.database.sqlalchemy_db import SQLAlchemyDatabase


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
