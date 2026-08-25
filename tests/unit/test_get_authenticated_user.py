from unittest.mock import AsyncMock, MagicMock

import pytest

from core.application.services.user_service import UserService
from core.domain.entities.user import User
from infra.drivers.api.dependencies.auth import get_authenticated_user


class TestGetAuthenticatedUser:

    @pytest.fixture
    def token_user(self) -> User:
        return User(
            uid="abc123", email="frodo@shire.com", email_verified=True, name="Frodo"
        )

    @pytest.fixture
    def user_service(self) -> UserService:
        mock = MagicMock(spec=UserService)
        mock.get_or_create_user = AsyncMock()
        return mock

    @pytest.mark.asyncio
    async def test_provisions_user_returned_by_verify_token(
        self, token_user: User, user_service: UserService
    ) -> None:
        user_service.get_or_create_user.return_value = token_user  # type: ignore

        result = await get_authenticated_user(
            user=token_user, user_service=user_service
        )

        user_service.get_or_create_user.assert_awaited_once_with(token_user)  # type: ignore
        assert result is token_user

    @pytest.mark.asyncio
    async def test_returns_persisted_user_from_service(
        self, token_user: User, user_service: UserService
    ) -> None:
        persisted_user = User(
            uid="abc123", email="frodo@shire.com", email_verified=True, name="Frodo"
        )
        user_service.get_or_create_user.return_value = persisted_user  # type: ignore

        result = await get_authenticated_user(
            user=token_user, user_service=user_service
        )

        assert result is persisted_user
