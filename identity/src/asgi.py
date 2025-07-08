import logging
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies.providers import get_database
from src.api.infrastructure import routes
from src.core.setup_logger import setup_logger
from src.settings import Settings

__all__ = (
    "create_app",
    "setup",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing database")

    database = get_database()
    await database.init_db()

    yield

    logger.info("Application shutdown, cleaning up resources")
    await database.close()
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    settings = setup()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app_api_cors_allowed_domains,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    root_router = routes.get_router()
    app.include_router(root_router)
    return app


def setup() -> Settings:
    load_dotenv(find_dotenv())
    settings = Settings.get()
    setup_logger(settings)

    logger.info(f"Application setup completed\nApplication: {settings.get_app_info()}")
    return settings
