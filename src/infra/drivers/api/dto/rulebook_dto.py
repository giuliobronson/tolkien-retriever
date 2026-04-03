from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.domain.enums import ProcessingStatus


class RulebookRequestDTO(BaseModel):
    game_name: str
    categories: List[str]
    min_players: int
    max_players: int
    playing_time: str


class RulebookResponseDTO(BaseModel):
    id: str
    game_name: str
    categories: List[str]
    min_players: int
    max_players: int
    playing_time: str
    creation_date: datetime
