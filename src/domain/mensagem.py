from dataclasses import dataclass, field
import datetime


@dataclass
class Mensagem:
    id: int
    autor: str
    conteudo: str
    crieada_em: datetime = field(default_factory=datetime.utcnow)