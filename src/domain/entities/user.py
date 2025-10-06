from domain.entities.author import Author


class User(Author): 
    def __init__(self, user_id: int, username: str) -> None:
        super().__init__(username)
        self.user_id = user_id