from langchain.agents import create_agent
from langchain.chat_models import BaseChatModel
from langchain_core.tools import tool
from langchain_core.vectorstores.base import VectorStore

from core.ports.llm.agent import IAgent
from core.ports.llm.agent_factory import IAgentFactory
from infra.adapters.llm.agents.rules_agent import RulesAgent
from infra.adapters.llm.prompts.utils import build_rules_agent_system_prompt


class RulesAgentFactory(IAgentFactory):
    def __init__(
        self, game_name: str, model: BaseChatModel, vector_store: VectorStore
    ) -> None:
        self.game_name = game_name
        self.llm = model
        self.vector_store = vector_store
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        vector_store = self.vector_store

        @tool
        def search_rulebook(query: str) -> str:
            """Busca trechos do manual oficial do jogo. Use quando o usuário perguntar
            sobre regras, mecânicas, setup, condições de vitória ou qualquer dúvida
            que exija consulta ao rulebook. Não use para perguntas gerais sobre
            estratégia ou opiniões da comunidade."""
            docs = vector_store.search(query=query, search_type="similarity")
            return "\n\n".join(doc.page_content for doc in docs)

        return create_agent(
            model=self.llm,
            tools=[search_rulebook],
            system_prompt=build_rules_agent_system_prompt(self.game_name),
        )

    def create(self) -> IAgent:
        return RulesAgent(self.workflow)
