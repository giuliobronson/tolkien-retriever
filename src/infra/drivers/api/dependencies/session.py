# Feature module: only imports leaf modules (repositories/storage/pipeline/agents) — never another feature module in dependencies/.
from fastapi import Depends

from core.application.services.session_service import SessionService
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.repositories.session_repository import ISessionRepository
from infra.drivers.api.dependencies.repositories import (
    get_rulebook_repository,
    get_session_repository,
)


async def get_session_service(
    session_repository: ISessionRepository = Depends(get_session_repository),
    rulebook_repository: IRulebookRepository = Depends(get_rulebook_repository),
):
    service = SessionService(session_repository, rulebook_repository)
    yield service
