# ingestion/loader.py

import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    """Load a PDF file and return list of pages"""
    
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
