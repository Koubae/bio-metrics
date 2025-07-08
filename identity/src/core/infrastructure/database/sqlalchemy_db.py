import typing as t
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import text
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.infrastructure.database.model import Base
from src.settings import Settings

logger = logging.getLogger(__name__)


class SQLAlchemyDatabase:
    DB_URI: t.ClassVar[str] = (
        "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    _singleton: t.ClassVar[t.Optional["SQLAlchemyDatabase"]] = None

    def __init__(
        self,
        uri: str,
        get_db_pool_size: int = 10,
        get_db_max_overflow: int = 5,
        pool_recycle: int = 3600,
        pool_pre_ping: bool = True,
        echo: bool = False,
    ) -> None:
        self._engine = create_async_engine(
            uri,
            pool_size=get_db_pool_size,
            max_overflow=get_db_max_overflow,
            pool_recycle=pool_recycle,
            poolclass=AsyncAdaptedQueuePool,
            pool_pre_ping=pool_pre_ping,
            echo=echo,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @classmethod
    def get(cls) -> "SQLAlchemyDatabase":
        if cls._singleton is None:
            settings: Settings = Settings.get()
            uri = cls.DB_URI.format(
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
                database=settings.db_name,
            )
            # fmt: off
            db_configs = {
                "uri"                : uri,
                "get_db_pool_size"   : settings.db_pool_size,
                "get_db_max_overflow": settings.db_max_overflow,
                "pool_recycle"       : settings.db_pool_recycle,
                "pool_pre_ping"      : settings.db_pool_pre_ping,
                "echo"               : settings.db_echo,
            }
            # fmt: on
            cls._singleton = cls(**db_configs)
            logger.info("Database manager initialized", extra={"extra": {**db_configs}})
        return cls._singleton

    @property
    def engine(self):
        if self._engine is None:
            raise RuntimeError("Database manager not initialized")
        return self._engine

    @property
    def session_factory(self):
        if self._session_factory is None:
            raise RuntimeError("Database manager not initialized")
        return self._session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession | Any, Any]:
        logger.debug("Creating database session...")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.exception(
                    f"Database session unhandled exception, rolling back, error: {e}",
                )
                await session.rollback()
                raise
            finally:
                await session.close()

        logger.debug("Database session closed")

    async def init_db(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.exception(f"Failed to create initialized database, error: {e}")
            raise

    async def drop_db(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.exception(f"Failed to drop database, error : {e}")
            raise

    async def health_check(self) -> bool:
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.exception(f"Database health check failed, error : {e}")
            return False

    async def reset_db(self):
        logger.info("Resetting database...")
        await self.drop_db()
        await self.init_db()
        logger.info("Database reset completed")

    async def close(self):
        if self._engine:
            await self._engine.dispose()
            logger.info("Database engine closed")
