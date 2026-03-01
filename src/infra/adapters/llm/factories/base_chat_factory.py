from langchain.chat_models import BaseChatModel
from langgraph.graph.state import START, END, StateGraph

from core.ports.llm.agent import IAgent
from core.ports.llm.agent_factory import IAgentFactory
from infra.adapters.llm.agents.base_chat_agent import BaseChatAgent
from infra.adapters.llm.state.chat_state import ChatState


class BaseChatFactory(IAgentFactory):
    def __init__(self, model: BaseChatModel) -> None:
        self.llm = model
        
    def generate(self, state: ChatState) -> ChatState:
        response = self.llm.invoke(state["messages"])
        state["messages"].append(response)
        return state
    
    def create(self) -> IAgent:
        workflow = StateGraph(ChatState)
        workflow.add_node("generate", self.generate)
        workflow.add_edge(START, "generate")
        workflow.add_edge("generate", END)
        return BaseChatAgent(workflow.compile())