from infra.adapters.repositories.session_repository.in_memory_session_repository import InMemorySessionRepository


async def get_session_repository():
    repository = InMemorySessionRepository()
    yield repository