from pathlib import Path

import chromadb
from src.config import settings


class VectorStore:
    def __init__(self, embedder):
        self.embedder = embedder
        persist_path = Path(settings.chroma_persist_directory)
        persist_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_path))
        self.collection = self.client.get_or_create_collection(settings.chroma_collection_name)

    def upsert(self, chunks):
        if not chunks:
            return
        embeddings = self.embedder.encode([c.text for c in chunks])
        self.collection.upsert(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[c.metadata for c in chunks],
            embeddings=embeddings,
        )

    def query(self, question: str, top_k: int):
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_embeddings=self.embedder.encode([question]),
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        return [
            {"id": i, "text": text, "metadata": metadata,
             "score": max(0.0, 1.0 - distance)}
            for i, text, metadata, distance in zip(
                result.get("ids", [[]])[0], result.get("documents", [[]])[0],
                result.get("metadatas", [[]])[0], result.get("distances", [[]])[0]
            )
        ]
