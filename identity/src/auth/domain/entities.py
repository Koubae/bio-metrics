from dataclasses import dataclass, field
from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    LAB_SCIENTIST = "lab_scientist"
    DOCTOR = "doctor"
    USER = "user"


@dataclass(frozen=True)
class AccessToken:
    access_token: str = field(repr=False)
    user_id: int
    username: str
    role: Role
    expires: float
