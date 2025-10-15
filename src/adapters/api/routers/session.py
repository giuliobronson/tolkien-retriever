from fastapi import APIRouter


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/")
async def get_sessions():
    return {"message": "List of sessions"}

@router.post("/")
async def create_session():
    return {"message": "Session created"}

@router.get("/{session_id}")
async def get_session(session_id: int):
    return {"message": f"Details of session {session_id}"}

@router.delete("/{session_id}")
async def delete_session(session_id: int):
    return {"message": f"Session {session_id} deleted"}