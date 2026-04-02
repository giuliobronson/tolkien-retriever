from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.domain.entities.session import Session
from core.domain.value_objects.message import Message
from core.domain.value_objects.role import Role
from infra.drivers.api.dependencies.services import (
    get_chat_service,
    get_session_service,
)
from infra.mappers.message_mapper import MessageMapper

router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/{rulebook_id}")
async def handle_query(
    websocket: WebSocket,
    rulebook_id: str,
    session_service: SessionService = Depends(get_session_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    await websocket.accept()
    session = await session_service.open_session(rulebook_id)
    chat_service.load_session(session)
    try:
        while True:
            data = await websocket.receive_json()
            query = Message(role=Role.USER, content=data["content"], timestamp=None)
            response = await chat_service.answer(query)
            await websocket.send_json(MessageMapper.to_dto(response).model_dump(mode="json"))

    except WebSocketDisconnect:
        print(f"Conexão fechada para o rulebook {rulebook_id}")
