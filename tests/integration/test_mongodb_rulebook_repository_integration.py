from datetime import datetime

import pytest

from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from core.ports.repositories.rulebook_repository import IRulebookRepository


class TestMongoDBRulebookRepositoryIntegration:

    @pytest.fixture
    def sample_rulebook(self) -> Rulebook:
        return Rulebook(
            hash="abc123def456",
            game_name="Player's Handbook",
            creation_date=datetime.now(),
            categories=["fantasy", "rpg"],
            number_of_players=4,
            img_path="/tmp/handbook.png",
            playing_time="2-3h",
            processing_status=ProcessingStatus.PENDING,
        )

    @pytest.mark.asyncio
    async def test_save_rulebook(
        self, rulebook_repository: IRulebookRepository, sample_rulebook: Rulebook
    ):
        # Arrange

        # Act
        result = await rulebook_repository.save(sample_rulebook)

        # Assert
        assert result is not None
        assert result.game_name == "Player's Handbook"

    @pytest.mark.asyncio
    async def test_find_by_id(
        self, rulebook_repository: IRulebookRepository, sample_rulebook: Rulebook
    ):
        # Arrange
        saved = await rulebook_repository.save(sample_rulebook)

        # Act
        found = await rulebook_repository.find_by_id(saved.hash)

        # Assert
        assert found is not None
        assert found.game_name == sample_rulebook.game_name

    @pytest.mark.asyncio
    async def test_find_all(
        self, rulebook_repository: IRulebookRepository, sample_rulebook: Rulebook
    ):
        # Arrange
        await rulebook_repository.save(sample_rulebook)

        # Act
        results = await rulebook_repository.find_all()

        # Assert
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_update(
        self, rulebook_repository: IRulebookRepository, sample_rulebook: Rulebook
    ):
        # Arrange
        saved = await rulebook_repository.save(sample_rulebook)
        sample_rulebook.game_name = "Updated Handbook"

        # Act
        await rulebook_repository.update(saved.hash, sample_rulebook)
        updated = await rulebook_repository.find_by_id(saved.hash)

        # Assert
        assert updated is not None
        assert updated.game_name == "Updated Handbook"

    @pytest.mark.asyncio
    async def test_delete(
        self, rulebook_repository: IRulebookRepository, sample_rulebook: Rulebook
    ):
        # Arrange
        insert_result = await rulebook_repository.save(sample_rulebook)
        rulebook_id = insert_result.hash

        # Act
        await rulebook_repository.delete(rulebook_id)
        found = await rulebook_repository.find_by_id(rulebook_id)

        # Assert
        assert found is None
