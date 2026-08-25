# Feature module: only imports leaf modules (repositories/storage/pipeline/agents) — never another feature module in dependencies/.
from fastapi import Depends

from core.application.services.rulebook_service import RulebookService
from core.ports.pipeline.rulebook_pipeline import IRulebookPipeline
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.storage.file_storage import IFileStorage
from infra.drivers.api.dependencies.pipeline import get_rulebook_pipeline
from infra.drivers.api.dependencies.repositories import get_rulebook_repository
from infra.drivers.api.dependencies.storage import get_file_storage


async def get_rulebook_service(
    storage: IFileStorage = Depends(get_file_storage),
    processer: IRulebookPipeline = Depends(get_rulebook_pipeline),
    repository: IRulebookRepository = Depends(get_rulebook_repository),
):
    service = RulebookService(storage, processer, repository)
    yield service
