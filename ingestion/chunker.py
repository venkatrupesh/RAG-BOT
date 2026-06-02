# ingestion/chunker.py
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("langchain_text_splitters not available")

import sys
sys.path.append(".")
from ingestion.loader import load_pdf

def chunk_documents(file_path: str, chunk_size=512, chunk_overlap=50):
    """Split PDF pages into smaller chunks"""
    
    if not LANGCHAIN_AVAILABLE:
        print("⚠️ Text splitter not available.")
        return []
    
    # Step 1: Load the PDF
    pages = load_pdf(file_path)
    
    if not pages:
        print("❌ No pages loaded. Check your PDF.")
        return []
    
    # Debug: check if pages have actual text
    print(f"\n🔍 Checking text content...")
    for i, page in enumerate(pages[:3]):
        print(f"Page {i+1} text length: {len(page.page_content)} chars")
        print(f"Page {i+1} preview: {page.page_content[:200]}")
        print("---")
    
    # Filter out empty pages
    pages = [p for p in pages if len(p.page_content.strip()) > 10]
    print(f"\n📄 Pages with actual text: {len(pages)}")
    
    if not pages:
        print("❌ No text found in PDF. It may be a scanned/image PDF.")
        return []
    
    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = splitter.split_documents(pages)
    
    print(f"\n✅ Chunking complete!")
    print(f"📦 Total chunks created: {len(chunks)}")
    
    if chunks:
        print(f"\n--- Preview of chunk 1 ---")
        print(chunks[0].page_content)
    
    return chunks

if __name__ == "__main__":
    chunks = chunk_documents("data/sample.pdf")
