import json
from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile

from core.application.services.rulebook_service import RulebookService
from core.domain.exceptions.invalid_rulebook_error import InvalidRulebookError
from core.domain.exceptions.rulebook_not_found_error import RulebookNotFoundError
from core.ports.repositories.rulebook_repository import IRulebookRepository
from infra.adapters.utils import calculate_file_hash
from infra.drivers.api.dependencies.repositories import get_rulebook_repository
from infra.drivers.api.dependencies.services import get_rulebook_service
from infra.drivers.api.dto.rulebook_dto import RulebookRequestDTO, RulebookResponseDTO
from infra.mappers.rulebook_mapper import RulebookMapper

router = APIRouter(prefix="/rulebooks", tags=["rulebook"])


@router.post("/upload")
async def upload_rulebook(
    metadata: str = Form(...),
    file: UploadFile = File(...),
    service: RulebookService = Depends(get_rulebook_service),
) -> None:
    metadata_dict = json.loads(metadata)
    metadata_obj = RulebookRequestDTO(**metadata_dict)

    content = await file.read()
    if not file.filename:
        raise InvalidRulebookError("Nome do arquivo é obrigatório")

    rulebook = RulebookMapper.dto_to_entity(metadata_obj, calculate_file_hash(content))
    await service.upload_rulebook(file.filename, content, file.content_type, rulebook)


@router.get("/")
async def get_rulebooks(
    repository: IRulebookRepository = Depends(get_rulebook_repository),
) -> List[RulebookResponseDTO]:
    rulebooks = await repository.find_all()
    return RulebookMapper.entities_to_dtos(rulebooks)


@router.get("/{rulebook_id}")
async def get_rulebook(
    rulebook_id: str, repository: IRulebookRepository = Depends(get_rulebook_repository)
) -> RulebookResponseDTO:
    rulebook = await repository.find_by_id(rulebook_id)

    if not rulebook:
        raise RulebookNotFoundError("Rulebook não encontrado")

    return RulebookMapper.entity_to_dto(rulebook)
