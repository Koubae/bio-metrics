import hashlib

from src.auth.domain.ports import PasswordHasher


class HashLibPasswordHasher(PasswordHasher):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.hash_password(plain_password) == hashed_password
