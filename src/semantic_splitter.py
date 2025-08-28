from typing import List
from langchain_text_splitters import TextSplitter


class SemanticSplitter(TextSplitter):
    """A text splitter that splits text based on semantic meaning."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        # Implement a semantic splitting algorithm here
        # For demonstration purposes, we'll use a simple placeholder
        sentences = text.split('. ')
        chunks = []
        current_chunk = []

        for sentence in sentences:
            if len(' '.join(current_chunk)) + len(sentence) + 1 <= self.chunk_size:
                current_chunk.append(sentence)
            else:
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]

        if current_chunk:
            chunks.append('. '.join(current_chunk))

        # Handle overlap
        final_chunks = []
        for i in range(len(chunks)):
            start_index = max(0, i - (self.chunk_overlap // self.chunk_size))
            end_index = min(len(chunks), i + 1)
            final_chunks.append(' '.join(chunks[start_index:end_index]))

        return final_chunks