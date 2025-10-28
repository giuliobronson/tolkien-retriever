from typing import List
from langgraph.graph.state import CompiledStateGraph

from adapters.llm.state.chat_state import ChatState
from adapters.mappers.message_mapper import MessageMapper
from core.application.ports.llm.agent import IAgent
from core.domain.value_objects.message import Message


class LangGraphAgent(IAgent):
    def __init__(self, graph: CompiledStateGraph) -> None:
        self.graph = graph
        self.state = ChatState()

    def set_state(self, history: List[Message]) -> None:
        self.state.messages = [MessageMapper.to_langgraph(message) for message in history]
    
    def answer(self, input: Message) -> Message:
        self.state["messages"].append(MessageMapper.to_langgraph(input))
        output = self.graph.invoke(self.state)
        self.state["messages"].append(output["messages"][-1])
        return MessageMapper.from_langgraph(output["messages"][-1])