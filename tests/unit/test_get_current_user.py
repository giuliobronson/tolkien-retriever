from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.security import HTTPAuthorizationCredentials

from core.domain.entities.user import User
from core.domain.exceptions.invalid_token_error import InvalidTokenError
from core.domain.exceptions.missing_token_error import MissingTokenError
from core.ports.auth.auth_service import IAuthService
from infra.drivers.api.dependencies.auth import get_current_user


class TestGetCurrentUser:

    @pytest.fixture
    def authenticated_user(self) -> User:
        return User(
            uid="abc123", email="frodo@shire.com", email_verified=True, name="Frodo"
        )

    @pytest.fixture
    def auth_service(self, authenticated_user: User) -> IAuthService:
        mock = MagicMock(spec=IAuthService)
        mock.verify_token = AsyncMock(return_value=authenticated_user)
        return mock

    @pytest.mark.asyncio
    async def test_missing_credentials_raises_missing_token_error(
        self, auth_service: IAuthService
    ) -> None:
        with pytest.raises(MissingTokenError):
            await get_current_user(credentials=None, auth_service=auth_service)  # type: ignore

        auth_service.verify_token.assert_not_awaited()  # type: ignore

    @pytest.mark.asyncio
    async def test_valid_credentials_delegates_to_auth_service(
        self, auth_service: IAuthService, authenticated_user: User
    ) -> None:
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="valid-token"
        )

        result = await get_current_user(
            credentials=credentials, auth_service=auth_service
        )

        auth_service.verify_token.assert_awaited_once_with("valid-token")  # type: ignore
        assert result is authenticated_user

    @pytest.mark.asyncio
    async def test_invalid_credentials_propagates_auth_service_error(
        self, auth_service: IAuthService
    ) -> None:
        auth_service.verify_token = AsyncMock(
            side_effect=InvalidTokenError("Token inválido")
        )
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="invalid-token"
        )

        with pytest.raises(InvalidTokenError):
            await get_current_user(credentials=credentials, auth_service=auth_service)
