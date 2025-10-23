from dataclasses import dataclass
import datetime

from core.domain.value_objects.author import Author

@dataclass
class Message:
    author: Author
    content: str
    timestamp: datetime.datetime
