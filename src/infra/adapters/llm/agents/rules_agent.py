from typing import AsyncIterator, List, Optional

from langchain.messages import AIMessageChunk
from langchain_core.messages import AIMessage, BaseMessage
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

    async def answer_stream(self, input: Message) -> AsyncIterator[str]:
        self.history.append(MessageMapper.to_langgraph(input))
        full_response = ""
        async for event in self.graph.astream_events(
            {"messages": self.history}, version="v2"
        ):
            if event["event"] == "on_chat_model_stream":
                chunk: Optional[AIMessageChunk] = event["data"].get("chunk")
                if chunk and isinstance(chunk.content, str) and chunk.content:
                    full_response += chunk.content
                    yield chunk.content
        self.history.append(AIMessage(content=full_response))
