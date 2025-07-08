from abc import ABC

from src.core.domain.ports import AsyncRepository


class AccountRepository(AsyncRepository, ABC):
    pass
