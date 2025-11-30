from langchain.chat_models import BaseChatModel
from langgraph.graph.state import START, END, StateGraph, CompiledStateGraph

from core.ports.llm.agent import IAgent
from core.ports.llm.agent_factory import IAgentFactory
from core.ports.vector_database.vector_database import IVectorDatabase
from infra.adapters.llm.agents.base_chat_agent import BaseChatAgent
from infra.adapters.llm.prompts.rag_prompt import build_expand_query
from infra.adapters.llm.state.rag_state import RagState


class RagFactory(IAgentFactory):
    def __init__(self, model: BaseChatModel, vector_database: IVectorDatabase) -> None:
        self.llm = model
        self.vector_database = vector_database

    def _expand_query(self, state: RagState) -> RagState:
        prompt = build_expand_query(state["messages"])
        query = self.llm.invoke(prompt)
        return {
            **state,
            "query": query
        }
    
    def _retrieve(self, state: RagState) -> RagState:
        documents = self.vector_database.similarity_search(state["query"], k=5)
        return {
            **state,
            "documents": documents
        }
        
    def _generate(self, state: RagState) -> RagState:
        response = self.llm.invoke(state["messages"])
        messages = state["messages"] + [response]
        return {
            **state,
            "messages": messages
        }
    
    def _build_workflow(self) -> CompiledStateGraph:
        workflow = StateGraph(RagState)
        workflow.add_node("_generate", self._generate)
        workflow.add_node("_retrieve", self._retrieve)
        workflow.add_node("_expand_query", self._expand_query)
        workflow.add_edge(START, "_expand_query")
        workflow.add_edge("_expand_query", "_retrieve")
        workflow.add_edge("_retrieve", "_generate")
        workflow.add_edge("_generate", END)
        return workflow.compile()
    
    def create(self) -> IAgent:
        return BaseChatAgent(self._build_workflow())