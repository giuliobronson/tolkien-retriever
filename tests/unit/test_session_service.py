from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.application.services.session_service import SessionService
from core.domain.entities.rulebook import Rulebook
from core.domain.entities.session import Session
from core.domain.enums import ProcessingStatus
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.repositories.session_repository import ISessionRepository


class TestSessionService:

    @pytest.fixture
    def session_repository(self) -> ISessionRepository:
        mock = MagicMock(spec=ISessionRepository)
        mock.find_by_rulebook_id_and_owner = AsyncMock(return_value=None)
        mock.find_all_by_owner_id = AsyncMock(return_value=[])
        mock.save = AsyncMock(side_effect=lambda entity: entity)
        return mock

    @pytest.fixture
    def rulebook_repository(self) -> IRulebookRepository:
        mock = MagicMock(spec=IRulebookRepository)
        mock.find_by_ids = AsyncMock(return_value=[])
        return mock

    @pytest.fixture
    def service(
        self,
        session_repository: ISessionRepository,
        rulebook_repository: IRulebookRepository,
    ) -> SessionService:
        return SessionService(session_repository, rulebook_repository)

    @pytest.mark.asyncio
    async def test_create_session_fills_owner_id(
        self, service: SessionService, session_repository: ISessionRepository
    ) -> None:
        session = await service.create_session("rulebook-1", "owner-1")

        assert session.rulebook_id == "rulebook-1"
        assert session.owner_id == "owner-1"
        session_repository.save.assert_awaited_once_with(session)  # type: ignore

    @pytest.mark.asyncio
    async def test_open_session_returns_existing_session_of_same_owner(
        self, service: SessionService, session_repository: ISessionRepository
    ) -> None:
        existing = Session(id="session-1", rulebook_id="rulebook-1", owner_id="owner-1")
        session_repository.find_by_rulebook_id_and_owner = AsyncMock(  # type: ignore
            return_value=existing
        )

        result = await service.open_session("rulebook-1", "owner-1")

        session_repository.find_by_rulebook_id_and_owner.assert_awaited_once_with(  # type: ignore
            "rulebook-1", "owner-1"
        )
        session_repository.save.assert_not_awaited()  # type: ignore
        assert result is existing

    @pytest.mark.asyncio
    async def test_open_session_creates_new_session_for_different_owner(
        self, service: SessionService, session_repository: ISessionRepository
    ) -> None:
        # Regressão: existir sessão de outro dono para o mesmo rulebook não pode
        # fazer o lookup "vazar" para um usuário diferente.
        session_repository.find_by_rulebook_id_and_owner = AsyncMock(  # type: ignore
            return_value=None
        )

        result = await service.open_session("rulebook-1", "owner-2")

        session_repository.find_by_rulebook_id_and_owner.assert_awaited_once_with(  # type: ignore
            "rulebook-1", "owner-2"
        )
        session_repository.save.assert_awaited_once_with(result)  # type: ignore
        assert result.owner_id == "owner-2"

    @pytest.mark.asyncio
    async def test_get_rulebooks_from_sessions_scoped_to_owner(
        self,
        service: SessionService,
        session_repository: ISessionRepository,
        rulebook_repository: IRulebookRepository,
    ) -> None:
        sessions = [
            Session(id="session-1", rulebook_id="rulebook-1", owner_id="owner-1"),
            Session(id="session-2", rulebook_id="rulebook-2", owner_id="owner-1"),
        ]
        rulebook = Rulebook(
            id="rulebook-1",
            hash="abc123",
            game_name="Lord of the Rings",
            creation_date=datetime(2024, 1, 1),
            categories=["adventure"],
            min_players=4,
            max_players=8,
            playing_time="90-120 min",
            processing_status=ProcessingStatus.PENDING,
        )
        session_repository.find_all_by_owner_id = AsyncMock(return_value=sessions)  # type: ignore
        rulebook_repository.find_by_ids = AsyncMock(return_value=[rulebook])  # type: ignore

        result = await service.get_rulebooks_from_sessions("owner-1")

        session_repository.find_all_by_owner_id.assert_awaited_once_with("owner-1")  # type: ignore
        called_ids = set(rulebook_repository.find_by_ids.call_args.args[0])  # type: ignore
        assert called_ids == {"rulebook-1", "rulebook-2"}
        assert result == [rulebook]
