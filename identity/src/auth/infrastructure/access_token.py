import hashlib
import logging
import typing as t
from datetime import datetime, timedelta, UTC

import jwt

from src.auth.domain.entities import AccessToken, Role
from src.auth.domain.exceptions import AuthAccessTokenInvalid, AuthAccessTokenExpired
from src.auth.domain.ports import PasswordHasher, AccessTokenGenerator
from src.settings import Settings

logger = logging.getLogger(__name__)


class HashLibPasswordHasher(PasswordHasher):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.hash_password(plain_password) == hashed_password


class JWTAccessTokenAuth(AccessTokenGenerator):
    JWT_ALGORITHM: t.ClassVar[str] = "RS256"

    def generate_access_token(
        self, user_id: int, username: str, role: Role
    ) -> AccessToken:
        settings = Settings.get()
        expires_seconds = (
            datetime.now(UTC) + timedelta(hours=settings.app_jwt_expiration_hours)
        ).timestamp()
        payload = {
            "sub": user_id,
            "exp": expires_seconds,
            "iat": datetime.now(UTC),
            "iss": "bio-metrics-identity",
            "role": str(role),
            "username": username,
        }
        token = jwt.encode(
            payload, settings.get_cert_private(), algorithm=self.JWT_ALGORITHM
        )
        access_token = AccessToken(
            user_id=user_id,
            username=username,
            role=role,
            expires=expires_seconds,
            access_token=token,
        )
        return access_token

    def parse_access_token(self, access_token: str) -> AccessToken:
        settings = Settings.get()
        try:
            payload = jwt.decode(
                access_token,
                settings.get_cert_public(),
                algorithms=[self.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            logger.debug(
                "Access-Token expired", extra={"extra": {"access_token": access_token}}
            )
            raise AuthAccessTokenExpired("Token expired")
        except jwt.InvalidTokenError:
            logger.debug(
                "Invalid Access-Token", extra={"extra": {"access_token": access_token}}
            )
            raise AuthAccessTokenInvalid("Invalid token")

        try:
            user_id: int = payload["sub"]
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
            user_id=user_id,
            username=username,
            role=Role(role),
            expires=expires,
            access_token=access_token,
        )
