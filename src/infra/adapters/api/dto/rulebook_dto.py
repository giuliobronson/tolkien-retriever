from datetime import datetime
from typing import List

from pydantic import BaseModel


class RulebookDTO(BaseModel):
    game_name: str
    categories: List[str]
    number_of_players: int
    playing_time: str
