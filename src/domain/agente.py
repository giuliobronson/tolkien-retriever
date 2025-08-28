from dataclasses import dataclass, field
from typing import List

from domain.conversa import Conversa


@dataclass
class Agente:
    id: int
    nome: str
    conversas: List["Conversa"] = field(default_factory=list)
    