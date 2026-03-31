from typing import Optional

from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from core.domain.exceptions.rulebook_not_processed import RulebookNotProcessed
from core.domain.exceptions.rulebook_processing_failed import RulebookProcessingFailed
from core.ports.pipeline.rulebook_pipeline import IRulebookPipeline
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.storage.file_storage import IFileStorage


class RulebookService:
    def __init__(
        self,
        storage: IFileStorage,
        pipeline: IRulebookPipeline,
        rulebook_repository: IRulebookRepository,
    ) -> None:
        self.storage = storage
        self.pipeline = pipeline
        self.rulebook_repository = rulebook_repository

    async def upload_rulebook(
        self,
        filename: str,
        content: bytes,
        content_type: Optional[str],
        rulebook: Rulebook,
    ) -> None:
        # Verificação da existência e status de processamento do arquivo
        result = await self.rulebook_repository.find_by_id(rulebook.hash)

        # Persistência dos metadados do Rulebook no banco de dados
        if result:
            if result.processing_status == ProcessingStatus.PENDING:
                raise RulebookNotProcessed(result.hash)
            else:
                await self.rulebook_repository.update(result.hash, rulebook)
        else:
            await self.rulebook_repository.save(rulebook)

        # Execução da pipeline de RAG e persistência do arquivo no storage
        try:
            await self.pipeline.execute(content, filename)
            await self.storage.upload(filename, content, content_type)
            rulebook.processing_status = ProcessingStatus.DONE
        except Exception:
            rulebook.processing_status = ProcessingStatus.ERROR
            raise RulebookProcessingFailed(rulebook.hash)
        finally:
            await self.rulebook_repository.update(rulebook.hash, rulebook)
