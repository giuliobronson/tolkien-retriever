from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from adapters.api.dto.message_dto import MessageDTO
from adapters.mappers.message_mapper import MessageMapper
from core.application.message_service import MessageService
from api.dependencies import get_message_service


router = APIRouter(prefix="/sessions/{session_id}/messages", tags=["messages"])


@router.get("/")
async def get_message_history(message_service=Depends(get_message_service)):
    return message_service.get_message_history()

@router.post("/")
async def send_message(
    request: MessageDTO,
    message_service: MessageService=Depends(get_message_service)
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