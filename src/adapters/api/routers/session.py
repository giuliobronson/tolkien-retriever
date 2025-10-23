from fastapi import APIRouter, Depends

from adapters.api.dependencies import get_session_service
from adapters.api.dto.message_dto import MessageDTO
from adapters.api.dto.session_dto import SessionDTO
from adapters.mappers.message_mapper import MessageMapper
from adapters.mappers.session_mapper import SessionMapper
from core.application.services.session_service import SessionService


router = APIRouter(prefix="/sessions", tags=["session"])


@router.post("/")
async def create_session(
    dto: MessageDTO, 
    session_service: SessionService=Depends(get_session_service)
) -> SessionDTO:
    return SessionMapper.to_dto(await session_service.create_session(MessageMapper.to_entity(dto)))

@router.get("/{session_id}")
async def open_session(
    session_id: int, 
    session_service: SessionService=Depends(get_session_service)
) -> SessionDTO:
    return SessionMapper.to_dto(await session_service.open_session(session_id))
