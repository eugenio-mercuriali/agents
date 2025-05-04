import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore


class ChromaDB:
    """ChromaDB class."""

    def __init__(self, persist_dir: str = "./chroma_db"):
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)

    def setup_vector_index(self, collection_name: str) -> VectorStoreIndex:
        """Set up a vector index with Chroma."""
        collection = self.chroma_client.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        return VectorStoreIndex.from_vector_store(vector_store)

    def add_embedding(self, doc_id, embedding, metadata=None):
        pass

    def search(self, query_embedding, top_k=5):
        pass
