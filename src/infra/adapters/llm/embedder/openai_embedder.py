from typing import List

from langchain_openai import OpenAIEmbeddings

from core.ports.llm.embedder import IEmbedder


class OpenAIEmbedder(IEmbedder):
    def __init__(self):
        self.embedder = OpenAIEmbeddings(model="text-embedding-3-small")

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.embed_documents(texts)
