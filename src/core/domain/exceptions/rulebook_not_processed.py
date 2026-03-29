class RulebookNotProcessed(Exception):
    def __init__(self, hash: str) -> None:
        super().__init__(f"Rulebook de id={hash} não teve o processamento finalizado")
        self.hash = hash
