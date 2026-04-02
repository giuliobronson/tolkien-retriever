from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.application.services.rulebook_service import RulebookService
from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from core.domain.exceptions.rulebook_not_processed import RulebookNotProcessed
from core.ports.pipeline.rulebook_pipeline import IRulebookPipeline
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.storage.file_storage import IFileStorage


class TestRulebookService:

    @pytest.fixture
    def rulebook(self) -> Rulebook:
        return Rulebook(
            id="test-rulebook-id",
            hash="abc123",
            game_name="Lord of the Rings",
            creation_date=datetime(2024, 1, 1),
            categories=["adventure"],
            min_players=4,
            max_players=8,
            playing_time="90-120 min",
            processing_status=ProcessingStatus.PENDING,
        )

    @pytest.fixture
    def storage(self) -> IFileStorage:
        mock = MagicMock(spec=IFileStorage)
        mock.upload = AsyncMock(return_value=None)
        return mock

    @pytest.fixture
    def processor(self) -> IRulebookPipeline:
        mock = MagicMock(spec=IRulebookPipeline)
        mock.execute = AsyncMock(return_value=None)
        return mock

    @pytest.fixture
    def rulebook_repository(self) -> IRulebookRepository:
        mock = MagicMock(spec=IRulebookRepository)
        mock.find_by_hash = AsyncMock(return_value=None)
        mock.save = AsyncMock(return_value=None)
        mock.update = AsyncMock(return_value=None)
        return mock

    @pytest.fixture
    def service(
        self,
        storage: IFileStorage,
        processor: IRulebookPipeline,
        rulebook_repository: IRulebookRepository,
    ) -> RulebookService:
        return RulebookService(
            storage=storage,
            pipeline=processor,
            rulebook_repository=rulebook_repository,
        )

    @pytest.mark.asyncio
    async def test_upload_new_rulebook_saves_and_processes(
        self,
        storage,
        processor,
        rulebook_repository,
        service: RulebookService,
        rulebook: Rulebook,
    ) -> None:
        await service.upload_rulebook(
            filename="lotr.pdf",
            content=b"pdf content",
            content_type="application/pdf",
            rulebook=rulebook,
        )

        rulebook_repository.save.assert_awaited_once_with(rulebook)
        rulebook_repository.update.assert_awaited_once_with(rulebook.id, rulebook)
        processor.execute.assert_awaited_once_with(b"pdf content", "lotr.pdf")
        storage.upload.assert_awaited_once_with(
            "lotr.pdf", b"pdf content", "application/pdf"
        )

    @pytest.mark.asyncio
    async def test_upload_rulebook_with_error_status_updates_and_processes(
        self,
        storage,
        processor,
        rulebook_repository,
        service: RulebookService,
        rulebook: Rulebook,
    ) -> None:
        existing = Rulebook(
            id="existing-rulebook-id",
            hash="abc123",
            game_name="Lord of the Rings",
            creation_date=datetime(2024, 1, 1),
            categories=["adventure"],
            min_players=4,
            max_players=8,
            playing_time="90-120 min",
            processing_status=ProcessingStatus.ERROR,
        )
        rulebook_repository.find_by_hash = AsyncMock(return_value=existing)

        await service.upload_rulebook(
            filename="lotr.pdf",
            content=b"pdf content",
            content_type="application/pdf",
            rulebook=rulebook,
        )

        assert rulebook_repository.update.await_count == 2
        rulebook_repository.save.assert_not_awaited()
        processor.execute.assert_awaited_once_with(b"pdf content", "lotr.pdf")
        storage.upload.assert_awaited_once_with(
            "lotr.pdf", b"pdf content", "application/pdf"
        )

    @pytest.mark.asyncio
    async def test_upload_rulebook_already_processing_raises(
        self,
        rulebook_repository,
        service: RulebookService,
        rulebook: Rulebook,
    ) -> None:
        existing = Rulebook(
            id="existing-rulebook-id",
            hash="abc123",
            game_name="Lord of the Rings",
            creation_date=datetime(2024, 1, 1),
            categories=["adventure"],
            min_players=4,
            max_players=8,
            playing_time="90-120 min",
            processing_status=ProcessingStatus.PENDING,
        )
        rulebook_repository.find_by_hash = AsyncMock(return_value=existing)

        with pytest.raises(RulebookNotProcessed):
            await service.upload_rulebook(
                filename="lotr.pdf",
                content=b"pdf content",
                content_type="application/pdf",
                rulebook=rulebook,
            )
