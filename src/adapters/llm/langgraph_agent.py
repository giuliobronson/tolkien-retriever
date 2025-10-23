from core.application.ports.llm.agent_graph import IAgentGraph
from langchain.chat_models import init_chat_model
from langgraph.graph import START, END, StateGraph


class LangGraphAgent(IAgentGraph):
    def __init__(self) -> None:
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph()

        workflow.add_edge(START, "chatbot")
        end_state = workflow.add_state(END)

        workflow.add_transition(
            start_state,
            end_state,
            action=lambda input: self.llm.invoke([HumanMessage(content=input["input"])]),
        )

        return workflow.compile()
    
    def run(self, input: str) -> str:
        result = self.graph.invoke({"input": input})
        return result["output"]