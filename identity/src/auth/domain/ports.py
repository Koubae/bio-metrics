from abc import ABC, abstractmethod

from src.auth.domain.entities import AccessToken


class PasswordHasher(ABC):
    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> str:
        ...

    @classmethod
    @abstractmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        ...


class AccessTokenGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_access_token(self, user_id: int, username: str, role: str) -> AccessToken:
        pass

    @classmethod
    @abstractmethod
    def parse_access_token(self, access_token: str) -> AccessToken:
        """
        Raises:
            - AuthAccessTokenInvalid: if the access token is invalid
            - AuthAccessTokenExpired: if the access token is expired
        """
        pass
