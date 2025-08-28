from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Documento:
    id: int
    titulo: str
    conteudo: str
    embedding: Optional[List[float]] = None