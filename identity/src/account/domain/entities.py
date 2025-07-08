from dataclasses import dataclass, field

from src.auth.domain.entities import Role
from src.core.domain.models import EntityTimestampedIdBase


@dataclass
class Account(EntityTimestampedIdBase):
    id: int | None
    username: str
    role: Role


@dataclass
class AccountWithPassword(Account):
    password: str = field(repr=False)
