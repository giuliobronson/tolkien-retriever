from dataclasses import dataclass
import datetime

from domain.entities.author import Author

@dataclass
class Message:
    author: Author
    content: str
    timestamp: datetime.datetime
