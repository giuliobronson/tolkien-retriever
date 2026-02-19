import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    MINIO_BUCKET_DOCUMENTS,
    MINIO_ENDPOINT_URL,
    MINIO_ROOT_PASSWORD,
    MINIO_ROOT_USER,
    MONGODB_DATABASE,
    MONGODB_URL,
)
from infra.adapters.repositories.rulebook.mongodb_rulebook_repository import (
    MongoDBRulebookRepository,
)
from infra.adapters.storage.minio_storage import MinIOStorage


@pytest.fixture(scope="session")
def minio_storage():
    storage = MinIOStorage(
        endpoint=MINIO_ENDPOINT_URL,
        access_key=MINIO_ROOT_USER,
        secret_key=MINIO_ROOT_PASSWORD,
        bucket_name=MINIO_BUCKET_DOCUMENTS,
        secure=False,
    )
    yield storage


@pytest_asyncio.fixture(scope="function")
async def rulebook_repository():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DATABASE]
    repo = MongoDBRulebookRepository(db)
    await repo.collection.delete_many({})
    yield repo
    await repo.collection.delete_many({})
    client.close()
