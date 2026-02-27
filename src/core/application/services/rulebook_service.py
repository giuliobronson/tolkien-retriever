from typing import Optional

from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from core.domain.exceptions.rulebook_not_processed import RulebookNotProcessed
from core.ports.processer.rulebook_processer import IRulebookProcesser
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.storage.file_storage import IFileStorage


class RulebookService:
    def __init__(
        self,
        storage: IFileStorage,
        processor: IRulebookProcesser,
        rulebook_repository: IRulebookRepository,
    ) -> None:
        self.storage = storage
        self.processor = processor
        self.rulebook_repository = rulebook_repository

    async def upload_rulebook(
        self,
        filename: str,
        content: bytes,
        content_type: Optional[str],
        rulebook: Rulebook,
    ) -> None:
        result = await self.rulebook_repository.find_by_id(rulebook.hash)

        if result and result.processing_status != ProcessingStatus.ERROR:
            raise RulebookNotProcessed(result.hash)

        if result and result.processing_status == ProcessingStatus.ERROR:
            await self.rulebook_repository.update(rulebook.hash, rulebook)
        else:
            await self.rulebook_repository.save(rulebook)

        await self.processor.process(content, filename)

        await self.storage.upload(filename, content, content_type)
