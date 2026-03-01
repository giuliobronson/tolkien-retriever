import tempfile
from collections.abc import AsyncIterator
from typing import Callable, Dict, Iterator, List, Optional

from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import DocItem
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document


class DoclingLoader(BaseLoader):

    def __init__(self, content: bytes, filename: str) -> None:
        self.content = content
        self.filename = filename
        self.converter = DocumentConverter()

    def lazy_load(self) -> Iterator[Document]:
        raise NotImplementedError("Use alazy_load().")

    async def alazy_load(self) -> AsyncIterator[Document]:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(self.content)
            tmp.flush()

            result = self.converter.convert(tmp.name)

        doc = result.document

        page_texts: Dict[int, List[str]] = {}
        page_tables: Dict[int, List[str]] = {}
        page_pictures: Dict[int, List[str]] = {}
        for element, _ in doc.iterate_items():
            if not isinstance(element, DocItem) or not element.prov:
                continue

            export_fn: Optional[Callable[[], str]] = getattr(
                element, "export_to_markdown", None
            )
            if export_fn is None:
                continue

            text = export_fn().strip()
            if not text:
                continue

            page_no = element.prov[0].page_no
            label = str(element.label).lower()

            if "table" in label:
                page_tables.setdefault(page_no, []).append(text)

            elif "picture" in label or "image" in label or "figure" in label:
                page_pictures.setdefault(page_no, []).append(text)

            else:
                page_texts.setdefault(page_no, []).append(text)

        # Yield texts
        for page_no in sorted(page_texts.keys()):
            text = "\n\n".join(page_texts[page_no]).strip()

            if text:
                yield Document(
                    page_content=text,
                    metadata={
                        "source": self.filename,
                        "page": page_no,
                        "type": "text",
                    },
                )

        # Yield tables
        for page_no, tables in page_tables.items():
            for i, table_md in enumerate(tables):
                yield Document(
                    page_content=table_md,
                    metadata={
                        "source": self.filename,
                        "page": page_no,
                        "type": "table",
                        "table_index": i,
                    },
                )

        # Yield images
        for page_no, pictures in page_pictures.items():
            for i, caption in enumerate(pictures):
                yield Document(
                    page_content=caption,
                    metadata={
                        "source": self.filename,
                        "page": page_no,
                        "type": "image",
                        "image_index": i,
                    },
                )
