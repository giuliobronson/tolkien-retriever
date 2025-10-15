from domain.entities.author import Author


class Agent(Author):
    def __init__(self, name: str) -> None:
        super().__init__(name)