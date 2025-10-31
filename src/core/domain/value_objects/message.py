from dataclasses import dataclass
import datetime
from typing import Optional

from core.domain.value_objects.role import Role


@dataclass
class Message:
    role: Role
    content: str
    timestamp: Optional[datetime.datetime]
