from datetime import datetime
from uuid import uuid4

from core.domain.entities.rulebook import Rulebook
from core.domain.enums import ProcessingStatus
from infra.drivers.api.dto.rulebook_dto import RulebookRequestDTO, RulebookResponseDTO


class RulebookMapper:
    @staticmethod
    def entity_to_document(rulebook: Rulebook) -> dict:
        return {
            "id": rulebook.id,
            "hash": rulebook.hash,
            "game_name": rulebook.game_name,
            "creation_date": rulebook.creation_date,
            "categories": rulebook.categories,
            "min_players": rulebook.min_players,
            "max_players": rulebook.max_players,
            "playing_time": rulebook.playing_time,
            "processing_status": rulebook.processing_status.value,
        }

    @staticmethod
    def document_to_entity(doc: dict) -> Rulebook:
        return Rulebook(
            id=doc["id"],
            hash=doc["hash"],
            game_name=doc["game_name"],
            creation_date=doc["creation_date"],
            categories=doc["categories"],
            min_players=doc["min_players"],
            max_players=doc["max_players"],
            playing_time=doc["playing_time"],
            processing_status=ProcessingStatus(doc["processing_status"]),
        )

    @staticmethod
    def dto_to_entity(dto: RulebookRequestDTO, hash: str) -> Rulebook:
        return Rulebook(
            id=str(uuid4()),
            hash=hash,
            creation_date=datetime.now(),
            processing_status=ProcessingStatus.PENDING,
            **dto.model_dump(),
        )

    @staticmethod
    def entity_to_dto(rulebook: Rulebook) -> RulebookResponseDTO:
        return RulebookResponseDTO(
            id=rulebook.id,
            game_name=rulebook.game_name,
            categories=rulebook.categories,
            min_players=rulebook.min_players,
            max_players=rulebook.max_players,
            playing_time=rulebook.playing_time,
            creation_date=rulebook.creation_date,
        )

    @staticmethod
    def entities_to_dtos(rulebooks: list[Rulebook]) -> list[RulebookResponseDTO]:
        return [RulebookMapper.entity_to_dto(rulebook) for rulebook in rulebooks]
