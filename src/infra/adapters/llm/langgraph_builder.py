from langchain.chat_models import BaseChatModel
from langgraph.graph.state import START, END, StateGraph, CompiledStateGraph

from infra.adapters.llm.state.chat_state import ChatState


class LangGraphBuilder:
    def __init__(self, model: BaseChatModel) -> None:
        self.llm = model
    def generate(self, state: ChatState) -> ChatState:
        response = self.llm.invoke(state["messages"])
        state["messages"].append(response)
        return state
    
    def build_graph(self) -> CompiledStateGraph:
        workflow = StateGraph(ChatState)
        workflow.add_node("generate", self.generate)
        workflow.add_edge(START, "generate")
        workflow.add_edge("generate", END)
        return workflow.compile()