class ApplicationError(Exception):
    def __init__(self, message: str, code: str | None = None, cause: Exception | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.cause = cause
        
    def __str__(self):
        return f"[{self.code}] {self.message}" if self.code else self.message