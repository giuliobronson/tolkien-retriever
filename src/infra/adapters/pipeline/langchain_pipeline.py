from langchain_core.vectorstores.base import VectorStore

from core.ports.pipeline.document_processor import IDocumentProcessor
from core.ports.pipeline.rulebook_pipeline import IRulebookPipeline


class LangChainPipeline(IRulebookPipeline):

    def __init__(self, processor: IDocumentProcessor, vector_store: VectorStore) -> None:
        self.processor = processor
        self.vector_store = vector_store

    async def execute(self, content: bytes, filename: str) -> None:
        chunks = await self.processor.process(content, filename)
        await self.vector_store.aadd_documents(chunks)
