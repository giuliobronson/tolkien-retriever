from datetime import datetime

from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from infra.adapters.api.dto.rulebook_dto import RulebookDTO


class RulebookMapper:
    @staticmethod
    def entity_to_document(rulebook: Rulebook) -> dict:
        return {
            "hash": rulebook.hash,
            "game_name": rulebook.game_name,
            "creation_date": rulebook.creation_date,
            "categories": rulebook.categories,
            "number_of_players": rulebook.number_of_players,
            "img_path": rulebook.img_path,
            "playing_time": rulebook.playing_time,
            "processing_status": rulebook.processing_status.value,
        }

    @staticmethod
    def document_to_entity(doc: dict) -> Rulebook:
        return Rulebook(
            hash=doc["hash"],
            game_name=doc["game_name"],
            creation_date=doc["creation_date"],
            categories=doc["categories"],
            number_of_players=doc["number_of_players"],
            img_path=doc["img_path"],
            playing_time=doc["playing_time"],
            processing_status=ProcessingStatus(doc["processing_status"]),
        )

    @staticmethod
    def dto_to_entity(dto: RulebookDTO, hash: str) -> Rulebook:
        return Rulebook(
            hash=hash,
            creation_date=datetime.now(),
            processing_status=ProcessingStatus.IN_PROGRESS,
            **dto.model_dump(),
        )
