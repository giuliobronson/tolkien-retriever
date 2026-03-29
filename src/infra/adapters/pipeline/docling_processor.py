from typing import List

from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from langchain_core.documents import Document

from core.ports.pipeline.document_processor import IDocumentProcessor
from infra.adapters.pipeline.docling_loader import DoclingLoader


class DoclingProcessor(IDocumentProcessor):

    async def process(self, content: bytes, filename: str) -> List[Document]:
        loader = DoclingLoader(content, filename)
        doc = await loader.aload()

        chunker = HybridChunker(repeat_table_header=True)
        chunks = []
        for chunk in chunker.chunk(doc):
            metadata = {
                "source": filename,
                **chunk.meta.export_json_dict(),
            }
            chunks.append(Document(page_content=chunk.text, metadata=metadata))
        return chunks
