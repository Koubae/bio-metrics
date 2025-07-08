from unittest.mock import patch

import jwt
import pytest

from src.auth.domain.exceptions import AuthAccessTokenExpired, AuthAccessTokenInvalid
from src.auth.infrastructure.access_token import JWTAccessTokenAuth


class TestJWTAccessTokenGenerator:

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
