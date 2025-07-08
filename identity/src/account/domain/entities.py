from dataclasses import dataclass

from src.auth.domain.entities import Role
from src.core.domain.models import EntityTimestampedIdBase


@dataclass
class Account(EntityTimestampedIdBase):
    id: int | None
    username: str
    role: Role
