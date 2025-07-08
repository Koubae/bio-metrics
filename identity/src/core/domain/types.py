from typing import TypeAlias, TypeVar, Union
from uuid import UUID

from src.core.domain.models import (
    DomainIdBase,
    DomainAuditBase,
    DomainTimestampedIdBase,
)

Domain = TypeVar(
    "Domain", bound=DomainIdBase | DomainAuditBase | DomainTimestampedIdBase
)
Model = TypeVar("Model")
DBSimplePrimaryKey: TypeAlias = Union[int, str, UUID]
DBCompositePrimaryKey: TypeAlias = dict[str, DBSimplePrimaryKey]
DBPrimaryKey: TypeAlias = Union[DBSimplePrimaryKey, DBCompositePrimaryKey]
