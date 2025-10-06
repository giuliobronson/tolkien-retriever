from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="/sessions/{session_id}/messages", tags=["messages"])


@router.get("/")
async def get_message_history():
    return {"message": "List of messages"}

@router.post("/")
async def send_message():
    return {"message": "Message sent"}

@router.websocket("/stream")
async def stream_response(websocket: WebSocket, session_id: int)
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{data}")

    except WebSocketDisconnect:
        print(f"Conexão fechada para a sessão {session_id}")