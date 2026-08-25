from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.application.services.user_service import UserService
from core.domain.entities.session import Session
from core.domain.entities.user import User
from core.domain.exceptions.expired_token_error import ExpiredTokenError
from core.domain.value_objects.message import Message
from core.domain.value_objects.role import Role
from core.ports.auth.auth_service import IAuthService
from infra.drivers.api.dependencies.chat import get_chat_service
from infra.drivers.api.dependencies.session import get_session_service
from infra.drivers.api.dependencies.user import get_auth_service, get_user_service
from main import app


class TestChatRouterAuth:

    @pytest.fixture(autouse=True)
    def clear_overrides(self):
        yield
        app.dependency_overrides.clear()

    @pytest.fixture
    def client(self) -> TestClient:
        return TestClient(app)

    @pytest.fixture
    def session(self) -> Session:
        return Session(id="session-1", rulebook_id="rulebook-1", messages=[])

    @pytest.fixture
    def session_service(self, session: Session) -> SessionService:
        mock = MagicMock(spec=SessionService)
        mock.open_session = AsyncMock(return_value=session)
        return mock

    @pytest.fixture
    def chat_service(self) -> ChatService:
        mock = MagicMock(spec=ChatService)
        mock.load_session = MagicMock(return_value=None)
        mock.answer = AsyncMock(
            return_value=Message(role=Role.ASSISTANT, content="42", timestamp=None)
        )
        return mock

    @pytest.fixture
    def user_service(self) -> UserService:
        mock = MagicMock(spec=UserService)
        mock.get_or_create_user = AsyncMock(side_effect=lambda user: user)
        return mock

    def test_missing_token_returns_401(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/chat/rulebook-1", json={"role": "user", "content": "oi"}
        )

        assert response.status_code == 401
        assert response.json() == {"message": "Token de autenticação não informado"}

    def test_auth_service_error_returns_401(self, client: TestClient) -> None:
        mock_auth_service = MagicMock(spec=IAuthService)
        mock_auth_service.verify_token = AsyncMock(
            side_effect=ExpiredTokenError("Token expirado")
        )
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

        response = client.post(
            "/api/v1/chat/rulebook-1",
            json={"role": "user", "content": "oi"},
            headers={"Authorization": "Bearer expired-token"},
        )

        assert response.status_code == 401
        assert response.json() == {"message": "Token expirado"}

    def test_valid_token_reaches_chat_service(
        self,
        client: TestClient,
        session: Session,
        session_service: SessionService,
        chat_service: ChatService,
        user_service: UserService,
    ) -> None:
        mock_auth_service = MagicMock(spec=IAuthService)
        mock_auth_service.verify_token = AsyncMock(return_value=User(uid="abc123"))
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        app.dependency_overrides[get_session_service] = lambda: session_service
        app.dependency_overrides[get_chat_service] = lambda: chat_service
        app.dependency_overrides[get_user_service] = lambda: user_service

        response = client.post(
            "/api/v1/chat/rulebook-1",
            json={"role": "user", "content": "oi"},
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 200
        assert response.json()["content"] == "42"
        mock_auth_service.verify_token.assert_awaited_once_with("valid-token")
        user_service.get_or_create_user.assert_awaited_once_with(User(uid="abc123"))  # type: ignore
        chat_service.load_session.assert_called_once_with(session)  # type: ignore
