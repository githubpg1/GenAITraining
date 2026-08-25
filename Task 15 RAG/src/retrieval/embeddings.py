from src.config import settings


class Embedder:
    def __init__(self, model_name: str | None = None):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name or settings.embedding_model)

    def encode(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True).tolist()
