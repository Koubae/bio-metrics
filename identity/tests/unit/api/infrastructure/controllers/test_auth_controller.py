# tests\test_auth_controller.py
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException
from src.account.application.account_service import AccountService
from src.api.infrastructure.controllers.auth_controller import AuthController
from src.auth.application.auth_handlers import (
    SignUpResponse,
    SignUpRequest,
    LoginRequest,
    LoginResponse,
)
from src.auth.application.auth_service import AuthService
from src.auth.domain.entities import Role
from src.auth.domain.exceptions import AuthPasswordInvalid
from src.core.domain.exceptions import RepositoryEntityNotFound


class TestAuthController:
    @pytest.mark.asyncio
    @patch(
        "src.api.infrastructure.controllers.auth_controller.provide_account_service",
        new_callable=AsyncMock,
    )
    async def test_signup_success(self, mock_account_service):
        mock_request = SignUpRequest(username="test", password="password123", role=None)
        mock_response = SignUpResponse(id=1, username="test", role=Role.USER)

        mock_service = AsyncMock()
        mock_service.create_account.return_value = mock_response
        mock_account_service.return_value = mock_service

        result = await AuthController.signup(request=mock_request, service=mock_service)
        assert result == mock_response

    @pytest.mark.asyncio
    @patch(
        "src.api.infrastructure.controllers.auth_controller.provide_account_service",
        new_callable=AsyncMock,
    )
    async def test_signup_duplicate_account(self, mock_account_service):
        mock_request = SignUpRequest(username="test", password="password123", role=None)

        mock_service = AsyncMock()
        mock_service.create_account.side_effect = HTTPException(
            status_code=409, detail="Account already exists"
        )
        mock_account_service.return_value = mock_service

        with pytest.raises(HTTPException) as exc:
            await AuthController.signup(request=mock_request, service=mock_service)

        assert exc.value.status_code == 409

    @pytest.mark.asyncio
    @patch(
        "src.api.infrastructure.controllers.auth_controller.provide_auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_success(self, mock_auth_service):
        mock_request = LoginRequest(username="test", password="password123")
        mock_response = LoginResponse(
            access_token="token123", role=Role.USER, expires=1234567890.0
        )

        mock_service = AsyncMock()
        mock_service.login.return_value = mock_response
        mock_auth_service.return_value = mock_service

        result = await AuthController.login(request=mock_request, service=mock_service)
        assert result == mock_response

    @pytest.mark.asyncio
    @patch(
        "src.api.infrastructure.controllers.auth_controller.provide_auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_account_does_not_exist(self, mock_auth_service):
        mock_request = LoginRequest(username="nonexistentuser", password="password123")

        mock_service = AsyncMock()
        mock_service.login.side_effect = RepositoryEntityNotFound(
            model=object, values=("nonexistentuser",)  # noqa
        )
        mock_auth_service.return_value = mock_service

        with pytest.raises(HTTPException) as exc:
            await AuthController.login(request=mock_request, service=mock_service)

        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    @patch(
        "src.api.infrastructure.controllers.auth_controller.provide_auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_invalid_credentials(self, mock_auth_service):
        mock_request = LoginRequest(username="wronguser", password="wrongpassword")

        mock_service = AsyncMock()
        mock_service.login.side_effect = AuthPasswordInvalid()
        mock_auth_service.return_value = mock_service

        with pytest.raises(HTTPException) as exc:
            await AuthController.login(request=mock_request, service=mock_service)

        assert exc.value.status_code == 401
