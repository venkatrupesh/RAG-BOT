# ingestion/embedder.py - FINAL VERSION
# Just drop files in data/ folder and run this script

import sys
import os
import shutil
sys.path.append(".")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    WebBaseLoader,
    TextLoader
)
from pathlib import Path

def load_all_resources(data_folder="data/"):
    """Automatically load ALL supported files from data/ folder"""
    
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )
    
    data_path = Path(data_folder)
    
    if not data_path.exists():
        print("❌ data/ folder not found")
        return []
    
    # ── PDFs ──────────────────────────────────────
    pdf_files = list(data_path.glob("*.pdf"))
    if pdf_files:
        print(f"\n📄 Found {len(pdf_files)} PDF file(s):")
        for pdf in pdf_files:
            try:
                print(f"   → Loading: {pdf.name}")
                loader = PyPDFLoader(str(pdf))
                pages = loader.load()
                pages = [p for p in pages if len(p.page_content.strip()) > 10]
                chunks = splitter.split_documents(pages)
                all_chunks.extend(chunks)
                print(f"   ✅ {len(chunks)} chunks added")
            except Exception as e:
                print(f"   ❌ Failed to load {pdf.name}: {e}")

    # ── Word Documents ─────────────────────────────
    docx_files = list(data_path.glob("*.docx"))
    if docx_files:
        print(f"\n📝 Found {len(docx_files)} Word file(s):")
        for docx in docx_files:
            try:
                print(f"   → Loading: {docx.name}")
                loader = Docx2txtLoader(str(docx))
                docs = loader.load()
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                print(f"   ✅ {len(chunks)} chunks added")
            except Exception as e:
                print(f"   ❌ Failed to load {docx.name}: {e}")

    # ── CSV Files ──────────────────────────────────
    csv_files = list(data_path.glob("*.csv"))
    if csv_files:
        print(f"\n📊 Found {len(csv_files)} CSV file(s):")
        for csv in csv_files:
            try:
                print(f"   → Loading: {csv.name}")
                loader = CSVLoader(str(csv))
                docs = loader.load()
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                print(f"   ✅ {len(chunks)} chunks added")
            except Exception as e:
                print(f"   ❌ Failed to load {csv.name}: {e}")

    # ── Text Files ─────────────────────────────────
    txt_files = list(data_path.glob("*.txt"))
    if txt_files:
        print(f"\n📃 Found {len(txt_files)} Text file(s):")
        for txt in txt_files:
            try:
                print(f"   → Loading: {txt.name}")
                loader = TextLoader(str(txt))
                docs = loader.load()
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                print(f"   ✅ {len(chunks)} chunks added")
            except Exception as e:
                print(f"   ❌ Failed to load {txt.name}: {e}")

    # ── URLs from urls.txt ─────────────────────────
    urls_file = data_path / "urls.txt"
    if urls_file.exists():
        print(f"\n🌐 Found urls.txt — loading URLs:")
        with open(urls_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            try:
                print(f"   → Loading: {url}")
                loader = WebBaseLoader(url)
                docs = loader.load()
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                print(f"   ✅ {len(chunks)} chunks added")
            except Exception as e:
                print(f"   ❌ Failed to load {url}: {e}")

    return all_chunks


def build_vector_store():
    """Build vector store from all resources in data/ folder"""

    print("=" * 50)
    print("🚀 Building Vector Store")
    print("=" * 50)

    # Load all resources
    all_chunks = load_all_resources()

    if not all_chunks:
        print("\n❌ No content found. Add files to data/ folder.")
        return None

    print(f"\n📊 Total chunks from all resources: {len(all_chunks)}")

    # Load embedding model
    print("\n🔄 Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    print("✅ Embedding model ready!")

    # Clear old vector store
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
        print("🗑️  Cleared old vector store")

    # Build new vector store
    print(f"\n⏳ Creating vectors... please wait...")
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        collection_name="interview_docs",
        persist_directory="./chroma_db"
    )

    print(f"\n✅ Vector store built successfully!")
    print(f"📊 Total vectors stored: {len(all_chunks)}")
    print(f"📁 Saved to: ./chroma_db")
    print("=" * 50)

    return vectorstore


if __name__ == "__main__":
    vectorstore = build_vector_store()

    if vectorstore:
        # Quick test
        print("\n🧪 Testing retrieval...")
        results = vectorstore.similarity_search("What is Python?", k=2)
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}: {doc.page_content[:200]}")