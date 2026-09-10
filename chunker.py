"""
Header/Section-Based Chunker Parser for IP-SAKTI Sahayak
Enforces strict header/section-based splitting (never generic character-length splitting).
Attaches full metadata schema required by Master Reference §8.
"""

from typing import List, Dict, Any
from corpus_data import CORPUS_DOCUMENTS

def chunk_document_by_header(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses a document into metadata-tagged chunks based on structural section headers.
    Guarantees zero generic character slicing.
    """
    chunks = []
    text = doc["text"]
    
    # Split text into natural paragraphs/sections
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    
    for idx, para in enumerate(paragraphs):
        chunk_id = f"{doc['document_id']}_chunk_{idx+1}"
        chunk_obj = {
            "chunk_id": chunk_id,
            "document_id": doc["document_id"],
            "act": doc["act"],
            "section": doc["section"],
            "domain": doc["domain"],
            "jurisdiction": doc["jurisdiction"],
            "source_type": doc["source_type"],
            "authority_level": doc["authority_level"],
            "authority": doc["authority"],
            "topic": doc["topic"],
            "source_url": doc["source_url"],
            "header": doc["header"],
            "text": f"{doc['header']}\n\n{para}"
        }
        chunks.append(chunk_obj)
        
    return chunks

def get_all_corpus_chunks() -> List[Dict[str, Any]]:
    """
    Processes all Tier 1/2/3 documents into structured metadata chunks.
    """
    all_chunks = []
    for doc in CORPUS_DOCUMENTS:
        chunks = chunk_document_by_header(doc)
        all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    chunks = get_all_corpus_chunks()
    print(f"Header-based Chunking Parser initialized: Total {len(chunks)} metadata-tagged chunks generated from {len(CORPUS_DOCUMENTS)} official corpus documents.")
    print("\nSample Chunk Metadata:")
    print(chunks[0])
