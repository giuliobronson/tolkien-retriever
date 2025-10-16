from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from adapters.api.dto.message_dto import MessageDTO
from adapters.mappers.message_mapper import MessageMapper
from adapters.ws.dependencies import get_message_service, get_session_service
from core.application.services.session_service import SessionService


router = APIRouter(prefix="/sessions", tags=["session", "message"])


@router.get("/{session_id}")
async def get_message_history(
    session_id: int,
    session_service: SessionService=Depends(get_session_service)
):
    return session_service.get_message_history(session_id)

@router.post("/{session_id}")
async def send_message(
    request: MessageDTO,
    session_id: int,
    message_service: SessionService=Depends(get_message_service)
):
    return MessageMapper.to_dto(message_service.send_message(MessageMapper.to_entity(request)))

@router.websocket("/stream")
async def stream_response(websocket: WebSocket, session_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{data}")

    except WebSocketDisconnect:
        print(f"Conexão fechada para a sessão {session_id}")