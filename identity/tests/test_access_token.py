from datetime import datetime, timedelta, UTC
from unittest.mock import patch

import jwt
import pytest

from src.auth.domain.entities import AccessToken
from src.auth.domain.exceptions import AuthAccessTokenExpired, AuthAccessTokenInvalid
from src.auth.infrastructure.access_token import JWTAccessTokenAuth


class TestJWTAccessTokenGenerator:

    def test_generate_access_token_creates_valid_token(self):
        generator = JWTAccessTokenAuth()

        token = generator.generate_access_token(
            user_id=1, username="user", role="admin"
        )
        assert isinstance(
            token, AccessToken
        ), "Generated token must be of type AccessToken"

        expected = (1, "user", "admin")
        assert expected == (
            token.user_id,
            token.username,
            token.role,
        ), "Generated token must have the correct values"

    def test_generated_token_has_valid_expiration(self):
        generator = JWTAccessTokenAuth()
        token = generator.generate_access_token(
            user_id=1, username="user", role="admin"
        )
        now = datetime.now(UTC)
        expiration_time = datetime.fromtimestamp(token.expires, tz=UTC)
        assert (
            expiration_time > now
        ), "Generated token must have a future expiration time"
        assert expiration_time <= now + timedelta(
            hours=1
        ), "Generated token must expire within the correct time frame"

    @patch("jwt.decode")
    def test_parse_access_token_raises_expired_error(self, mock_decode):
        generator = JWTAccessTokenAuth()
        mock_decode.side_effect = jwt.ExpiredSignatureError
        with pytest.raises(AuthAccessTokenExpired):
            generator.parse_access_token("expired_token")

    @patch("jwt.decode")
    def test_parse_access_token_raises_invalid_error(self, mock_decode):
        generator = JWTAccessTokenAuth()
        mock_decode.side_effect = jwt.InvalidTokenError
        with pytest.raises(AuthAccessTokenInvalid):
            generator.parse_access_token("invalid_token")
