from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> str:
        ...

    @classmethod
    @abstractmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        ...
