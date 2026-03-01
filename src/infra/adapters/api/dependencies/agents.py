from qdrant_client import QdrantClient
from config import OPENAI_API_KEY
from infra.adapters.llm.factories.base_chat_factory import BaseChatFactory
from infra.adapters.llm.factories.rag_factory import RagFactory

from langchain.chat_models import init_chat_model


async def get_base_chat_agent():
    agent_factory = BaseChatFactory(
        init_chat_model(
            model="gpt-4o-mini", 
            model_provider="openai", 
            api_key=OPENAI_API_KEY, 
            temperature=0.7
        )
    )
    agent = agent_factory.create()
    yield agent

# async def get_agent():
#     agent_factory = RagFactory(
#         init_chat_model(
#             model="gpt-4o-mini", 
#             model_provider="openai", 
#             api_key=OPENAI_API_KEY, 
#             temperature=0.7
#         ),
#         QdrantClient()
#     )
#     agent = agent_factory.create()
#     yield agent