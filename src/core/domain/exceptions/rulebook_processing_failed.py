class RulebookProcessingFailed(Exception):
    def __init__(self, hash: str) -> None:
        super().__init__(f"Erro no processamento do Rulebook de id={hash}")
        self.hash = hash