# retrieval/retriever.py

import sys
sys.path.append(".")
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def load_vector_store(collection_name="interview_docs"):
    """Load existing vector store from disk"""
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore


def retrieve_context(query: str, k=4):
    """Search vector store and return top k relevant chunks"""
    
    print(f"\n🔍 Searching for: '{query}'")
    
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=k)
    
    print(f"📌 Found {len(results)} relevant chunks\n")
    
    # Combine all chunks into one context string
    context = "\n\n".join([doc.page_content for doc in results])
    
    return context


if __name__ == "__main__":
    test_queries = [
        "What is Python?",
        "What is a decorator?",
        "Difference between list and tuple?"
    ]
    
    for query in test_queries:
        print("=" * 50)
        context = retrieve_context(query)
        print(context[:400])
        print()
