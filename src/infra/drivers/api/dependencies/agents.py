from fastapi import Depends
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from config import EMBEDDING_MODEL, OPENAI_API_KEY, QDRANT_URL, RULEBOOK_COLLETION
from core.ports.repositories.rulebook_repository import IRulebookRepository
from infra.adapters.llm.factories.rules_agent_factory import RulesAgentFactory
from infra.drivers.api.dependencies.repositories import get_rulebook_repository


async def get_agent(
    rulebook_id: str,
    rulebook_repository: IRulebookRepository = Depends(get_rulebook_repository),
):
    rulebook = await rulebook_repository.find_by_id(rulebook_id)
    if not rulebook:
        raise ValueError(f"Rulebook {rulebook_id} não encontrado")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = QdrantVectorStore(
        client=QdrantClient(url=QDRANT_URL),
        collection_name=RULEBOOK_COLLETION,
        embedding=embeddings,
    )

    model = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        api_key=OPENAI_API_KEY,
        temperature=0.7,
    )

    agent_factory = RulesAgentFactory(
        game_name=rulebook.game_name,
        model=model,
        vector_store=vector_store,
        rulebook_hash=rulebook.hash,
    )

    yield agent_factory.create()
