from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True, kw_only=True)
class DomainIdBase(ABC):
    id: int | None = field(default=None)

    def has_id(self) -> bool:
        return self.id is not None

    def set_id(self, _id: int) -> None:
        self.id = _id


@dataclass(slots=True, kw_only=True)
class DomainAuditBase(ABC):
    created: datetime | None = field(default=None)
    updated: datetime | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class DomainTimestampedIdBase(DomainIdBase):
    created: datetime | None = field(default=None)
    updated: datetime | None = field(default=None)
