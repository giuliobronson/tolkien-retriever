import asyncio
import tempfile
from typing import List

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.doc_chunk import DocMeta
from docling_core.transforms.chunker.hierarchical_chunker import (
    ChunkingDocSerializer,
    ChunkingSerializerProvider,
)
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.serializer.markdown import MarkdownParams
from docling_core.types.doc.base import ImageRefMode
from docling_core.types.doc.document import DoclingDocument
from langchain_core.documents import Document

from core.ports.pipeline.document_processor import IDocumentProcessor
from infra.adapters.utils import calculate_file_hash


class TraversePicturesSerializerProvider(ChunkingSerializerProvider):
    def get_serializer(self, doc: DoclingDocument) -> ChunkingDocSerializer:
        return ChunkingDocSerializer(
            doc=doc,
            params=MarkdownParams(
                image_mode=ImageRefMode.PLACEHOLDER,
                image_placeholder="",
                escape_underscores=False,
                escape_html=False,
                traverse_pictures=True,
            ),
        )


class DoclingProcessor(IDocumentProcessor):

    def __init__(self) -> None:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        self.chunker = HybridChunker(
            repeat_table_header=True,
            serializer_provider=TraversePicturesSerializerProvider(),
        )

    async def process(self, content: bytes, filename: str) -> List[Document]:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            result = await asyncio.to_thread(self.converter.convert, tmp.name)
        doc = result.document

        chunks = []
        for chunk in self.chunker.chunk(doc):
            if not chunk.text.strip():
                continue

            page_no = None
            if isinstance(chunk.meta, DocMeta) and chunk.meta.doc_items[0].prov:
                page_no = chunk.meta.doc_items[0].prov[0].page_no

            metadata = {
                "hash": calculate_file_hash(content),
                "source": filename,
                "page_no": page_no,
            }

            chunks.append(
                Document(
                    page_content=self.chunker.contextualize(chunk),
                    metadata=metadata,
                )
            )

        return chunks
