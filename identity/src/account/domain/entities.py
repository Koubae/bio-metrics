from dataclasses import dataclass

from src.auth.domain.entities import Role


@dataclass(frozen=True)
class Account:
    id: int
    username: str
    role: Role
