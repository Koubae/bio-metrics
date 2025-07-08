import logging
import typing as t

import jwt

from src.auth.domain.entities import AccessToken, Role
from src.auth.domain.exceptions import AuthAccessTokenInvalid, AuthAccessTokenExpired
from src.auth.domain.ports import AccessTokenGenerator
from src.settings import Settings

logger = logging.getLogger(__name__)


class JWTAccessTokenAuth(AccessTokenGenerator):
    JWT_ALGORITHM: t.ClassVar[str] = "RS256"

    def parse_access_token(self, access_token: str) -> AccessToken:
        settings = Settings.get()
        try:
            payload = jwt.decode(
                access_token,
                settings.get_cert_public(),
                algorithms=[self.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError as error:
            logger.debug(
                "Access-Token expired",
                extra={"extra": {"access_token": access_token, "error": repr(error)}},
            )
            raise AuthAccessTokenExpired("Token expired")
        except jwt.InvalidTokenError as error:
            logger.info(
                "Invalid Access-Token",
                extra={"extra": {"access_token": access_token, "error": repr(error)}},
            )
            raise AuthAccessTokenInvalid("Invalid token")

        try:
            user_id: str = payload["sub"]
            username: str = payload["username"]
            role: str = payload["role"]
            expires: int = payload["exp"]
        except KeyError as error:
            logger.warning(
                f"Invalid Access-Token while parsing, error: {error}",
                extra={
                    "extra": {
                        "access_token": access_token,
                        "payload": payload,
                        "error": repr(error),
                    }
                },
            )
            raise AuthAccessTokenInvalid(f"Invalid token payload: {error}") from error

        return AccessToken(
            user_id=int(user_id),
            username=username,
            role=Role(role),
            expires=expires,
            access_token=access_token,
        )
