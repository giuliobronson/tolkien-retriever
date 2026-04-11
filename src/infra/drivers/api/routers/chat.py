from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.domain.value_objects.message import Message
from core.domain.value_objects.role import Role
from infra.drivers.api.dependencies.services import (
    get_chat_service,
    get_session_service,
)
from infra.drivers.api.dto.message_dto import MessageDTO
from infra.mappers.message_mapper import MessageMapper

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{rulebook_id}", response_model=MessageDTO)
async def handle_query(
    rulebook_id: str,
    body: MessageDTO,
    session_service: SessionService = Depends(get_session_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    session = await session_service.open_session(rulebook_id)
    chat_service.load_session(session)
    query = Message(role=Role.USER, content=body.content, timestamp=datetime.now())
    response = await chat_service.answer(query)
    return MessageMapper.to_dto(response)


@router.post("/{rulebook_id}/stream")
async def handle_query_stream(
    rulebook_id: str,
    body: MessageDTO,
    session_service: SessionService = Depends(get_session_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    session = await session_service.open_session(rulebook_id)
    chat_service.load_session(session)
    query = Message(role=Role.USER, content=body.content, timestamp=datetime.now())

    async def token_generator():
        async for token in chat_service.answer_stream(query):
            yield f"data: {token}\n\n"

    return StreamingResponse(token_generator(), media_type="text/event-stream")
