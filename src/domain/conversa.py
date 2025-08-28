from dataclasses import dataclass, field
import datetime

from domain.agente import Agente
from domain.mensagem import Mensagem


@dataclass
class Conversa:
    id: int
    titulo: str
    agente: Agente
    mensagens: list["Mensagem"] = field(default_factory=list)
    criada_em: datetime = field(default_factory=datetime.utcnow)
    atualizada_em: datetime = field(default_factory=datetime.utcnow)
    status: str = "ativa"