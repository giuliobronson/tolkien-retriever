class SessionNotFoundError(Exception):
    def __init__(self, session_id: str) -> None:
        super().__init__(f"Session with id={session_id} not found.")
        self.session_id = session_id