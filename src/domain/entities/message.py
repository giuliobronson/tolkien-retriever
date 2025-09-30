import datetime

from domain.entities.author import Author


class Message:
    def __init__(self, author: Author, content: str, timestamp: datetime.datetime) -> None:
        self.author = author
        self.content = content
        self.timestamp = timestamp
