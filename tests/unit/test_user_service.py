from unittest.mock import AsyncMock, MagicMock

import pytest

from core.application.services.user_service import UserService
from core.domain.entities.user import User
from core.domain.exceptions.user_not_found_error import UserNotFoundError
from core.ports.auth.auth_service import IAuthService
from core.ports.repositories.user_repository import IUserRepository


class TestUserService:

    @pytest.fixture
    def token_user(self) -> User:
        return User(
            uid="abc123", email="frodo@shire.com", email_verified=True, name="Frodo"
        )

    @pytest.fixture
    def user_repository(self) -> IUserRepository:
        return MagicMock(spec=IUserRepository)

    @pytest.fixture
    def auth_service(self) -> IAuthService:
        mock = MagicMock(spec=IAuthService)
        mock.delete_user = AsyncMock()
        return mock

    @pytest.fixture
    def user_service(
        self, user_repository: IUserRepository, auth_service: IAuthService
    ) -> UserService:
        return UserService(user_repository, auth_service)

    @pytest.mark.asyncio
    async def test_creates_user_when_not_found(
        self,
        user_service: UserService,
        user_repository: IUserRepository,
        token_user: User,
    ) -> None:
        user_repository.find_by_id = AsyncMock(return_value=None)  # type: ignore
        user_repository.save = AsyncMock(return_value=token_user)  # type: ignore

        result = await user_service.get_or_create_user(token_user)

        user_repository.find_by_id.assert_awaited_once_with("abc123")  # type: ignore
        user_repository.save.assert_awaited_once_with(token_user)  # type: ignore
        assert result is token_user

    @pytest.mark.asyncio
    async def test_returns_existing_user_without_saving(
        self,
        user_service: UserService,
        user_repository: IUserRepository,
        token_user: User,
    ) -> None:
        existing_user = User(
            uid="abc123", email="frodo@shire.com", email_verified=True, name="Frodo"
        )
        user_repository.find_by_id = AsyncMock(return_value=existing_user)  # type: ignore
        user_repository.save = AsyncMock()  # type: ignore

        result = await user_service.get_or_create_user(token_user)

        user_repository.find_by_id.assert_awaited_once_with("abc123")  # type: ignore
        user_repository.save.assert_not_awaited()  # type: ignore
        assert result is existing_user

    @pytest.mark.asyncio
    async def test_deletes_existing_user(
        self,
        user_service: UserService,
        user_repository: IUserRepository,
        auth_service: IAuthService,
        token_user: User,
    ) -> None:
        user_repository.find_by_id = AsyncMock(return_value=token_user)  # type: ignore
        user_repository.delete = AsyncMock()  # type: ignore

        await user_service.delete_account("abc123")

        user_repository.find_by_id.assert_awaited_once_with("abc123")  # type: ignore
        auth_service.delete_user.assert_awaited_once_with("abc123")  # type: ignore
        user_repository.delete.assert_awaited_once_with("abc123")  # type: ignore

    @pytest.mark.asyncio
    async def test_raises_when_deleting_unknown_user(
        self,
        user_service: UserService,
        user_repository: IUserRepository,
        auth_service: IAuthService,
    ) -> None:
        user_repository.find_by_id = AsyncMock(return_value=None)  # type: ignore
        user_repository.delete = AsyncMock()  # type: ignore

        with pytest.raises(UserNotFoundError):
            await user_service.delete_account("abc123")

        auth_service.delete_user.assert_not_awaited()  # type: ignore
        user_repository.delete.assert_not_awaited()  # type: ignore
