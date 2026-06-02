# ingestion/loader.py

import os

try:
    from langchain_community.document_loaders import PyPDFLoader
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("langchain_community not available")

def load_pdf(file_path: str):
    """Load a PDF file and return list of pages"""
    
    if not LANGCHAIN_AVAILABLE:
        print("⚠️ PyPDFLoader not available. Install langchain-community to use this feature.")
        return []
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []
    
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    print(f"✅ Loaded: {file_path}")
    print(f"📄 Total pages: {len(pages)}")
    print(f"\n--- Preview (first 500 chars) ---")
    print(pages[0].page_content[:500])
    
    return pages

if __name__ == "__main__":
    # Test it
    pages = load_pdf("data/sample.pdf")
