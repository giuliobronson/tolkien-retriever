class RulebookNotProcessed(Exception):
    def __init__(self, hash: str) -> None:
        super().__init__(f"Rulebook with id={hash} processing not finished yet.")
        self.hash = hash
