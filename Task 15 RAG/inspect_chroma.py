"""Print a non-secret inventory of the persistent policy collection."""
import chromadb
from src.config import settings

client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
collection = client.get_or_create_collection(settings.chroma_collection_name)
items = collection.get(include=["metadatas"])
metadata = items.get("metadatas", [])
print(f"collection={collection.name}")
print(f"count={collection.count()}")
print("source_files=")
for source in sorted({item.get("source_file", "<missing>") for item in metadata}):
    print(f"- {source}")
print("document_versions=")
for name, version in sorted({(item.get("document_name", "<missing>"), item.get("version", "<missing>")) for item in metadata}):
    print(f"- {name} | {version}")
