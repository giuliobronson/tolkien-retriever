import pytest

from core.domain.entities.user import User
from core.ports.repositories.user_repository import IUserRepository


class TestMongoDBUserRepositoryIntegration:

    @pytest.fixture
    def sample_user(self) -> User:
        return User(
            uid="abc123def456",
            email="frodo@shire.example",
            email_verified=True,
            name="Frodo Baggins",
        )

    @pytest.mark.asyncio
    async def test_save_user(self, user_repository: IUserRepository, sample_user: User):
        # Arrange

        # Act
        result = await user_repository.save(sample_user)

        # Assert
        assert result is not None
        assert result.name == "Frodo Baggins"

    @pytest.mark.asyncio
    async def test_find_by_id(
        self, user_repository: IUserRepository, sample_user: User
    ):
        # Arrange
        saved = await user_repository.save(sample_user)

        # Act
        found = await user_repository.find_by_id(saved.uid)

        # Assert
        assert found is not None
        assert found.email == sample_user.email

    @pytest.mark.asyncio
    async def test_find_all(self, user_repository: IUserRepository, sample_user: User):
        # Arrange
        await user_repository.save(sample_user)

        # Act
        results = await user_repository.find_all()

        # Assert
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_update(self, user_repository: IUserRepository, sample_user: User):
        # Arrange
        saved = await user_repository.save(sample_user)
        sample_user.name = "Frodo of the Nine Fingers"

        # Act
        await user_repository.update(saved.uid, sample_user)
        updated = await user_repository.find_by_id(saved.uid)

        # Assert
        assert updated is not None
        assert updated.name == "Frodo of the Nine Fingers"

    @pytest.mark.asyncio
    async def test_delete(self, user_repository: IUserRepository, sample_user: User):
        # Arrange
        insert_result = await user_repository.save(sample_user)
        user_uid = insert_result.uid

        # Act
        await user_repository.delete(user_uid)
        found = await user_repository.find_by_id(user_uid)

        # Assert
        assert found is None
