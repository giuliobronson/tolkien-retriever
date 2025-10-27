from dataclasses import dataclass
import datetime

from core.domain.value_objects.role import Role


@dataclass
class Message:
    role: Role
    content: str
    timestamp: datetime.datetime
