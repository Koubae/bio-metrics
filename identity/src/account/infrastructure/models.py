from sqlalchemy import Column, String
from sqlalchemy import Enum

from src.auth.domain.entities import Role
from src.core.infrastructure.database.model import TimestampedIdModel


class Account(TimestampedIdModel):
    __tablename__ = "account"

    username = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role, name="role_enum"), nullable=False, default=Role.USER)
