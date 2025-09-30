from domain.entities.agent import Agent
from ports.repositories.session_repository import ISessionRepository


class HandleUserQuery:
    def __init__(self, agent: Agent, session_repository: ISessionRepository) -> None:
        self.agent = agent
        self.session_repository = session_repository

    def execute(self, session_id: int, user_message: str) -> str:
        session = self.session_repository.get_session(session_id)
        response = self.agent.respond(user_message, session.messages)
        session.messages.append(response)
        self.session_repository.save_session(session)
        return response.content