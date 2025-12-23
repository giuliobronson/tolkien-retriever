from fastapi import APIRouter, Depends, File, UploadFile

from core.ports.storage.file_storage import IFileStorage


router = APIRouter(prefix="/rulebooks", tags=["rulebook"])


@router.post("/upload")
async def upload_rulebook(
    file: UploadFile=File(...),
    storage: IFileStorage=Depends()
):
    pass