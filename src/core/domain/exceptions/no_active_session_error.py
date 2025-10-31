class NoActiveSessionError(Exception):
    def __init__(self, message: str = "Nenhuma sessão ativa disponível"):
        super().__init__(message)