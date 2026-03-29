from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from config import EMBEDDING_MODEL, QDRANT_URL, RULEBOOK_COLLETION
from infra.adapters.pipeline.docling_processor import DoclingProcessor
from infra.adapters.pipeline.langchain_pipeline import LangChainPipeline


async def get_rulebook_pipeline():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(
        client=client, collection_name=RULEBOOK_COLLETION, embedding=embeddings
    )

    pipeline = LangChainPipeline(
        processor=DoclingProcessor(),
        vector_store=vector_store,
    )

    yield pipeline
