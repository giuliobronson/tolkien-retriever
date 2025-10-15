from application.use_cases.exceptions import ApplicationError
from ports.repositories.session_repository import ISessionRepository


class OpenSession:
    def __init__(self, session_repository: ISessionRepository) -> None:
        self.session_repository = session_repository
    
    def execute(self, session_id: int) -> SessionDTO:
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ApplicationError(
                message=f"Session {session_id} not found",
                code="SESSION_NOT_FOUND"
            )
        return session
