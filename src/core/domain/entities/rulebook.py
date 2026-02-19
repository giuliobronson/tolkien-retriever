from dataclasses import dataclass
from datetime import datetime
from typing import List

from core.domain.enums import ProcessingStatus
from core.domain.exceptions.invalid_rulebook_error import InvalidRulebookError


@dataclass
class Rulebook:
    hash: str
    game_name: str
    creation_date: datetime
    categories: List[str]
    number_of_players: (
        int  # Deveria ser um string com o range? Ou deveria ter o min e máx
    )
    img_path: str
    playing_time: str  # Deveria ser um string com o range? Ou deveria ter o min e máx
    processing_status: ProcessingStatus

    def __post_init__(self):
        self._validate_game_name()
        self._validate_hash()
        self._validate_number_of_players()

    def _validate_game_name(self):
        if not self.game_name or not self.game_name.strip():
            raise InvalidRulebookError("Game name must not be empty")

    def _validate_hash(self):
        if not self.hash or not self.hash.strip():
            raise InvalidRulebookError("Hash must not be empty")

    def _validate_number_of_players(self):
        if self.number_of_players <= 0:
            raise InvalidRulebookError("Number of players must be positive")
