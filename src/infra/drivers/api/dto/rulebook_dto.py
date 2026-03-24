from typing import List

from pydantic import BaseModel


class RulebookDTO(BaseModel):
    game_name: str
    categories: List[str]
    min_players: int
    max_players: int
    playing_time: str
