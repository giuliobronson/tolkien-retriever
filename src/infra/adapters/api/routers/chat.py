from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from infra.adapters.api.dependencies import get_chat_service, get_session_service
from infra.adapters.api.dto.message_dto import MessageDTO
from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.domain.value_objects.message import Message
from core.domain.entities.session import Session
from infra.mappers.message_mapper import MessageMapper


router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/{session_id}")
async def handle_query(
    websocket: WebSocket, 
    session_id: str, 
    session_service: SessionService=Depends(get_session_service),
    chat_service: ChatService=Depends(get_chat_service)
):
    await websocket.accept()
    session: Session = await session_service.open_session(session_id)
    chat_service.load_session(session)
    try:
        while True:
            data = await websocket.receive_json()
            response: Message = await chat_service.answer(MessageMapper.to_entity(MessageDTO(**data)))
            await websocket.send_json(MessageMapper.to_dto(response).model_dump_json())

    except WebSocketDisconnect:
        print(f"Conexão fechada para a sessão {session_id}")