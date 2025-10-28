from langchain.chat_models import init_chat_model
from langgraph.graph.state import START, END, StateGraph, CompiledStateGraph

from adapters.llm.state.chat_state import ChatState


class LangGraphBuilder:
    def __init__(self) -> None:
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)

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