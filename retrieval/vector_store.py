"""ChromaDB vector store setup."""

import chromadb
from typing import List


class VectorStore:
    """Manage vector storage with ChromaDB."""
    
    def __init__(self, collection_name: str = "interview_docs"):
        """Initialize ChromaDB client and collection.
        
        Args:
            collection_name: Name of the collection
        """
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    def add_chunks(self, chunks: List[dict]):
        """Add chunks to the vector store.
        
        Args:
            chunks: List of chunk dictionaries with 'text', 'embedding', and metadata
        """
        ids = [f"{chunk['source']}_{chunk['chunk_id']}" for chunk in chunks]
        embeddings = [chunk["embedding"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": chunk["source"], "chunk_id": chunk["chunk_id"]} for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
    
    def query(self, query_embedding: List[float], n_results: int = 3) -> dict:
        """Query the vector store.
        
        Args:
            query_embedding: Embedding vector for the query
            n_results: Number of results to return
            
        Returns:
            Query results from ChromaDB
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
