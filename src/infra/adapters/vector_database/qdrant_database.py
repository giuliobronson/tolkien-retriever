from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from core.domain.entities.document import Document
from core.ports.vector_database.vector_database import IVectorDatabase


class QdrantDatabase(IVectorDatabase):
    def __init__(self, client: QdrantClient, collection_name: str, embedder):
        self.client = client
        self.collection = collection_name
        self.embedder = embedder

    async def add(self, documents: List[Document]) -> None:
        points = []
        for doc in documents:
            embedding = self.embedder.embed(doc.content)
            points.append(
                PointStruct(
                    id=doc.id,
                    vector=embedding,
                    payload={"content": doc.content, "metadata": doc.metadata or {}},
                )
            )
        self.client.upsert(collection_name=self.collection, points=points)

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        embedding = self.embedder.embed(query)
        hits = self.client.search(
            collection_name=self.collection, query_vector=embedding, limit=k
        )
        results = [
            Document(
                id=str(hit.id),
                content=hit.payload["content"],
                metadata=hit.payload.get("metadata"),
            )
            for hit in hits
        ]

        return results

    async def delete(self, doc_id: str) -> None:
        self.client.delete(
            collection_name=self.collection, points_selector={"points": [doc_id]}
        )
