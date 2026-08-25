from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from core.application.services.session_service import SessionService
from core.application.services.user_service import UserService
from core.domain.entities.session import Session
from core.domain.entities.user import User
from core.domain.value_objects.message import Message
from core.domain.value_objects.role import Role
from core.ports.auth.auth_service import IAuthService
from core.ports.repositories.session_repository import ISessionRepository
from infra.drivers.api.dependencies.repositories import get_session_repository
from infra.drivers.api.dependencies.session import get_session_service
from infra.drivers.api.dependencies.user import get_auth_service, get_user_service
from main import app


class TestSessionRouter:

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
        return mock

    @pytest.fixture
    def session_service(self) -> SessionService:
        mock = MagicMock(spec=SessionService)
        mock.get_rulebooks_from_sessions = AsyncMock(return_value=[])
        return mock

    @pytest.fixture
    def session_repository(self) -> ISessionRepository:
        return MagicMock(spec=ISessionRepository)

    def _authenticate(self, token_user: User, user_service: UserService) -> None:
        mock_auth_service = MagicMock(spec=IAuthService)
        mock_auth_service.verify_token = AsyncMock(return_value=token_user)
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        app.dependency_overrides[get_user_service] = lambda: user_service

    def test_get_session_history_missing_token_returns_401(
        self, client: TestClient
    ) -> None:
        response = client.get("/api/v1/sessions/session-1")

        assert response.status_code == 401

    def test_get_rulebooks_from_sessions_missing_token_returns_401(
        self, client: TestClient
    ) -> None:
        response = client.get("/api/v1/sessions/rulebooks")

        assert response.status_code == 401

    def test_owner_reads_own_session_history(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
        session_repository: ISessionRepository,
    ) -> None:
        self._authenticate(token_user, user_service)
        session = Session(
            id="session-1",
            rulebook_id="rulebook-1",
            owner_id="abc123",
            messages=[Message(role=Role.USER, content="oi", timestamp=None)],
        )
        session_repository.find_by_id = AsyncMock(return_value=session)  # type: ignore
        app.dependency_overrides[get_session_repository] = lambda: session_repository

        response = client.get(
            "/api/v1/sessions/session-1",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 200
        assert response.json()[0]["content"] == "oi"

    def test_non_owner_reading_session_gets_404(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
        session_repository: ISessionRepository,
    ) -> None:
        self._authenticate(token_user, user_service)
        someone_elses_session = Session(
            id="session-1", rulebook_id="rulebook-1", owner_id="someone-else"
        )
        session_repository.find_by_id = AsyncMock(  # type: ignore
            return_value=someone_elses_session
        )
        app.dependency_overrides[get_session_repository] = lambda: session_repository

        response = client.get(
            "/api/v1/sessions/session-1",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 404

    def test_get_rulebooks_from_sessions_scopes_to_authenticated_user(
        self,
        client: TestClient,
        token_user: User,
        user_service: UserService,
        session_service: SessionService,
    ) -> None:
        self._authenticate(token_user, user_service)
        app.dependency_overrides[get_session_service] = lambda: session_service

        response = client.get(
            "/api/v1/sessions/rulebooks",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 200
        session_service.get_rulebooks_from_sessions.assert_awaited_once_with(  # type: ignore
            "abc123"
        )
