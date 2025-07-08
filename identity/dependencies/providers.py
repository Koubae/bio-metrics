from src.core.infrastructure.database.sqlalchemy_db import SQLAlchemyDatabase


def get_database() -> SQLAlchemyDatabase:
    database = SQLAlchemyDatabase.get()
    return database
