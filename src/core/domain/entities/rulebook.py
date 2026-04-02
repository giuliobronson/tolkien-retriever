from dataclasses import dataclass
from datetime import datetime
from typing import List

from core.domain.enums import ProcessingStatus
from core.domain.exceptions.invalid_rulebook_error import InvalidRulebookError


@dataclass
class Rulebook:
    id: str
    hash: str
    game_name: str
    creation_date: datetime
    categories: List[str]
    min_players: int
    max_players: int
    playing_time: str
    processing_status: ProcessingStatus

    def __post_init__(self):
        self._validate_game_name()
        self._validate_hash()
        self._validate_number_of_players()

    def _validate_game_name(self):
        if not self.game_name or not self.game_name.strip():
            raise InvalidRulebookError("Nome do jogo não pode ser vazio")

    def _validate_hash(self):
        if not self.hash or not self.hash.strip():
            raise InvalidRulebookError("Hash não pode ser vazio")

    def _validate_number_of_players(self):
        if self.min_players <= 0 and self.max_players >= self.min_players:
            raise InvalidRulebookError("Número de jogadores deve ser válido")
