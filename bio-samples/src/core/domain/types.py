from typing import TypeAlias, TypeVar, Union
from uuid import UUID

from src.core.domain.models import (
    EntityIdBase,
    EntityAuditBase,
    EntityTimestampedIdBase,
)

Entity = TypeVar(
    "Entity", bound=EntityIdBase | EntityAuditBase | EntityTimestampedIdBase
)
Model = TypeVar("Model")
DBSimplePrimaryKey: TypeAlias = Union[int, str, UUID]
DBCompositePrimaryKey: TypeAlias = dict[str, DBSimplePrimaryKey]
DBPrimaryKey: TypeAlias = Union[DBSimplePrimaryKey, DBCompositePrimaryKey]
