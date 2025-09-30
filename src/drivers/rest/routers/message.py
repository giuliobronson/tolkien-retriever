from fastapi import APIRouter


router = APIRouter(prefix="/sessions/{session_id}/messages", tags=["messages"])


@router.get("/")
async def get_message_history():
    return {"message": "List of messages"}

@router.post("/")
async def send_message():
    return {"message": "Message sent"}