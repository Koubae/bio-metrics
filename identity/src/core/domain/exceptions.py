from src.core.domain.types import Entity
from src.core.infrastructure.database.model import DbModel


class RepositoryException(Exception):
    pass


class RepositoryCreateException(RepositoryException):
    def __init__(self, model: type[DbModel], domain: Entity, error: str) -> None:
        super().__init__(
            f"Error while inserting {model} with values {domain}, error: {error}"
        )


class RepositoryPKMissingException(RepositoryException):
    def __init__(self, model: type[DbModel], missing: str) -> None:
        super().__init__(
            f"Missing primary-key column for model {model}, missing: '{missing}'"
        )
