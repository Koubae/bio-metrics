from abc import ABC, abstractmethod

from src.auth.domain.entities import AccessToken


class AccessTokenGenerator(ABC):
    @abstractmethod
    def parse_access_token(self, access_token: str) -> AccessToken:
        """
        Raises:
            - AuthAccessTokenInvalid: if the access token is invalid
            - AuthAccessTokenExpired: if the access token is expired
        """
        pass
