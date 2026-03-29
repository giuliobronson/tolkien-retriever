import asyncio
import tempfile

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.document import DoclingDocument


class DoclingLoader:

    def __init__(self, content: bytes, filename: str) -> None:
        self.content = content
        self.filename = filename
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        self.converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )

    async def aload(self) -> DoclingDocument:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(self.content)
            tmp.flush()
            result = await asyncio.to_thread(self.converter.convert, tmp.name)
        return result.document
