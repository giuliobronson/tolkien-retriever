from typing import List

from fastapi import APIRouter, Depends

from core.application.services.session_service import SessionService
from infra.drivers.api.dependencies.services import get_session_service
from infra.drivers.api.dto.rulebook_dto import RulebookResponseDTO
from infra.mappers.rulebook_mapper import RulebookMapper

router = APIRouter(prefix="/sessions", tags=["session"])


@router.get("/rulebooks")
async def get_rulebooks_from_sessions(
    service: SessionService = Depends(get_session_service),
) -> List[RulebookResponseDTO]:
    rulebooks = await service.get_rulebooks_from_sessions()
    return RulebookMapper.entities_to_dtos(rulebooks)
