from typing import List

from langchain_core.messages import BaseMessage
from langgraph.graph.state import CompiledStateGraph

from core.domain.value_objects.message import Message
from core.ports.llm.agent import IAgent
from infra.mappers.message_mapper import MessageMapper


class RulesAgent(IAgent):
    def __init__(self, graph: CompiledStateGraph) -> None:
        self.graph = graph
        self.history: List[BaseMessage] = []

    def set_history(self, history: List[Message]) -> None:
        self.history = [MessageMapper.to_langgraph(message) for message in history]

    def get_history(self) -> List[Message]:
        return MessageMapper.history_from_langgraph(self.history)

    async def answer(self, input: Message) -> Message:
        self.history.append(MessageMapper.to_langgraph(input))
        output = await self.graph.ainvoke({"messages": self.history})
        self.history = output["messages"]
        response = self.history[-1]
        return MessageMapper.from_langgraph(response)
