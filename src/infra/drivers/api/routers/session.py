from typing import List

from fastapi import APIRouter, Depends

from core.application.services.session_service import SessionService
from core.domain.entities.user import User
from core.domain.exceptions.session_not_found_error import SessionNotFoundError
from core.ports.repositories.session_repository import ISessionRepository
from infra.drivers.api.dependencies.repositories import get_session_repository
from infra.drivers.api.dependencies.session import get_session_service
from infra.drivers.api.dependencies.user import get_authenticated_user
from infra.drivers.api.dto.message_dto import MessageDTO
from infra.drivers.api.dto.rulebook_dto import RulebookResponseDTO
from infra.mappers.message_mapper import MessageMapper
from infra.mappers.rulebook_mapper import RulebookMapper

router = APIRouter(prefix="/sessions", tags=["session"])


@router.get("/rulebooks")
async def get_rulebooks_from_sessions(
    current_user: User = Depends(get_authenticated_user),
    service: SessionService = Depends(get_session_service),
) -> List[RulebookResponseDTO]:
    rulebooks = await service.get_rulebooks_from_sessions(current_user.uid)
    return RulebookMapper.entities_to_dtos(rulebooks)


@router.get("/{session_id}")
async def get_session_history(
    session_id: str,
    current_user: User = Depends(get_authenticated_user),
    repository: ISessionRepository = Depends(get_session_repository),
) -> List[MessageDTO]:
    session = await repository.find_by_id(session_id)
    if not session or session.owner_id != current_user.uid:
        raise SessionNotFoundError(f"Sessão não encontrada para o ID: {session_id}")
    return [MessageMapper.to_dto(message) for message in session.messages]
