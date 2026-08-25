from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from core.application.services.user_service import UserService
from core.domain.entities.user import User
from core.domain.exceptions.user_not_found_error import UserNotFoundError
from core.ports.auth.auth_service import IAuthService
from infra.drivers.api.dependencies.user import get_auth_service, get_user_service
from main import app


class TestUserRouter:

    @pytest.fixture(autouse=True)
    def clear_overrides(self):
        yield
        app.dependency_overrides.clear()

    @pytest.fixture
    def client(self) -> TestClient:
        return TestClient(app)

    @pytest.fixture
    def token_user(self) -> User:
        return User(uid="abc123", email="frodo@shire.com", email_verified=True)

    @pytest.fixture
    def user_service(self, token_user: User) -> UserService:
        mock = MagicMock(spec=UserService)
        mock.get_or_create_user = AsyncMock(return_value=token_user)
        mock.delete_account = AsyncMock()
        return mock

    def _authenticate(self, token_user: User, user_service: UserService) -> None:
        mock_auth_service = MagicMock(spec=IAuthService)
        mock_auth_service.verify_token = AsyncMock(return_value=token_user)
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        app.dependency_overrides[get_user_service] = lambda: user_service

    def test_missing_token_returns_401(self, client: TestClient) -> None:
        response = client.delete("/api/v1/user/abc123")

        assert response.status_code == 401
        assert response.json() == {"message": "Token de autenticação não informado"}

    def test_deletes_own_account(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
    ) -> None:
        self._authenticate(token_user, user_service)

        response = client.delete(
            "/api/v1/user/abc123",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 204
        user_service.delete_account.assert_awaited_once_with("abc123")  # type: ignore

    def test_cannot_delete_another_users_account(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
    ) -> None:
        self._authenticate(token_user, user_service)

        response = client.delete(
            "/api/v1/user/someone-else",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 403
        user_service.delete_account.assert_not_awaited()  # type: ignore

    def test_returns_404_when_user_not_found(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
    ) -> None:
        self._authenticate(token_user, user_service)
        user_service.delete_account = AsyncMock(  # type: ignore
            side_effect=UserNotFoundError("Usuário não encontrado: abc123")
        )

        response = client.delete(
            "/api/v1/user/abc123",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 404
        assert response.json() == {"message": "Usuário não encontrado: abc123"}
