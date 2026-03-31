import asyncio
import tempfile
from typing import List

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.doc_chunk import DocMeta
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from langchain_core.documents import Document

from core.ports.pipeline.document_processor import IDocumentProcessor
from infra.adapters.utils import calculate_file_hash


class DoclingProcessor(IDocumentProcessor):

    def __init__(self) -> None:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        self.converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )
        self.chunker = HybridChunker(repeat_table_header=True)

    async def process(self, content: bytes, filename: str) -> List[Document]:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            result = await asyncio.to_thread(self.converter.convert, tmp.name)
        doc = result.document

        chunks = []
        for chunk in self.chunker.chunk(doc):
            page_no = None
            if isinstance(chunk.meta, DocMeta) and chunk.meta.doc_items[0].prov:
                page_no = chunk.meta.doc_items[0].prov[0].page_no
            metadata = {
                "hash": calculate_file_hash(content),
                "source": filename,
                "page_no": page_no,
            }
            chunks.append(Document(page_content=chunk.text, metadata=metadata))
        return chunks
