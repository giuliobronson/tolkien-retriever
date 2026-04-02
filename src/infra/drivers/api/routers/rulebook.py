import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from core.application.services.rulebook_service import RulebookService
from infra.adapters.utils import calculate_file_hash
from infra.drivers.api.dependencies.services import get_rulebook_service
from infra.drivers.api.dto.rulebook_dto import RulebookDTO
from infra.mappers.rulebook_mapper import RulebookMapper

router = APIRouter(prefix="/rulebooks", tags=["rulebook"])


@router.post("/upload")
async def upload_rulebook(
    metadata: str = Form(...),
    file: UploadFile = File(...),
    service: RulebookService = Depends(get_rulebook_service),
):
    metadata_dict = json.loads(metadata)
    metadata_obj = RulebookDTO(**metadata_dict)

    content = await file.read()
    if not file.filename:

        raise HTTPException(400, "Nome do arquivo é obrigatório")
    rulebook = RulebookMapper.dto_to_entity(metadata_obj, calculate_file_hash(content))
    await service.upload_rulebook(file.filename, content, file.content_type, rulebook)
