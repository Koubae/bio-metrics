from src.core.domain.types import Entity
from src.core.infrastructure.database.model import DbModel


class RepositoryException(Exception):
    pass


class RepositoryDatabaseConnectionError(RepositoryException):
    def __init__(self, model: type[DbModel], entity: Entity, error: str) -> None:
        super().__init__(
            f"Database connection Error {model} with values {entity}, error: {error}"
        )


class RepositoryCreateException(RepositoryException):
    def __init__(
        self,
        model: type[DbModel],
        entity: Entity,
        error: str,
        message: str | None = None,
    ) -> None:
        message = message or f"Error while inserting {model} with values {entity}"
        super().__init__(message)


class RepositoryDuplicateRowException(RepositoryCreateException):
    def __init__(self, model: type[DbModel], entity: Entity, error: str) -> None:
        super().__init__(
            model,
            entity,
            error,
            f"RepositoryDuplicateRowException for {model} with values {entity}",
        )


class RepositoryPKMissingException(RepositoryException):
    def __init__(self, model: type[DbModel], missing: str) -> None:
        super().__init__(
            f"Missing primary-key column for model {model}, missing: '{missing}'"
        )
