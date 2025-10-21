from fastapi import WebSocket
from core.application.services.session_service import SessionService


class SessionWebSocketHandler:
    def __init__(self, session_service: SessionService) -> None:
        self.session_service = session_service
        
    async def handle_message(self, websocket: WebSocket, session_id: int):
        await websocket.accept()
        session = await self.session_service.open_session(session_id)
        try:
            while True:
                data = await websocket.receive_text()
                