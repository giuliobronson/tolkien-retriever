from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from adapters.api.dto.message_dto import MessageDTO
from adapters.mappers.message_mapper import MessageMapper
from adapters.ws.dependencies import get_message_service, get_session_service
from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.domain.entities.message import Message
from core.domain.entities.session import Session


router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/{session_id}")
async def handle_query(
    websocket: WebSocket, 
    session_id: str, 
    session_service: SessionService=Depends(get_session_service),
    chat_service: ChatService=Depends()
    ):
    await websocket.accept()
    session: Session = await session_service.open_session(session_id)
    try:
        while True:
            data = await websocket.receive_json()
            response: Message = await chat_service.handle_query(session, MessageMapper.to_entity(MessageDTO(**data)))
            await websocket.send_json(MessageMapper.to_dto(response).model_dump)

    except WebSocketDisconnect:
        print(f"Conexão fechada para a sessão {session_id}")