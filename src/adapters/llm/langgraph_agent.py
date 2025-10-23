from typing import List
from core.application.ports.llm.agent import IAgentGraph
from langchain.chat_models import init_chat_model
from langgraph.graph import START, END, StateGraph

from core.domain.value_objects.message import Message


class ChatState:
    messages: List[Message] = []
    

class LangGraphAgent(IAgentGraph):
    def __init__(self) -> None:
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)
        self.graph = self._build_graph()
        self.state = ChatState()
        
    def set_state(self, history: List[Message]):
        self.state.messages = history
        
    def input(self, state: ChatState) -> ChatState:
        state.messages.append(state.user_message)
        return state
        
    def reply(self, state: ChatState) -> ChatState:
        response = self.llm.invoke(state.messages)
        state.messages.append

    def _build_graph(self):
        workflow = StateGraph()

        workflow.add_edge(START, "chatbot")
        end_state = workflow.add_state(END)

        workflow.add_transition(
            start_state,
            end_state,
            action=lambda input: self.llm.invoke([HumanMessage(content=input["input"])]),
        )

        # return workflow.compile()
    
    def answer(self, input: Message) -> str:
        result = self.graph.invoke({"input": input})
        return result["output"]