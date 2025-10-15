from domain.entities.user import User


class Session:
    def __init__(self, user: User, title: str) -> None:
        self.user = user
        self.title = title
        self.messages = []