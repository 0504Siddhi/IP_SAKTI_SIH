"""
Chroma Vector Database Ingestion Script for IP-SAKTI Sahayak
Initializes local persistent Chroma DB in './chroma_db', creates collection 'ip_sakti_corpus',
and indexes all metadata-tagged chunks.
"""

import os
import chromadb
from chunker import get_all_corpus_chunks

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def run_ingestion():
    print(f"Initializing local persistent Chroma DB at: {DB_DIR}")
    client = chromadb.PersistentClient(path=DB_DIR)
    
    collection_name = "ip_sakti_corpus"
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    chunks = get_all_corpus_chunks()
    print(f"Ingesting {len(chunks)} metadata-tagged chunks into '{collection_name}'...")
    
    ids = []
    documents = []
    metadatas = []
    
    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        metadatas.append({
            "document_id": chunk["document_id"],
            "act": chunk["act"],
            "section": chunk["section"],
            "domain": chunk["domain"],
            "jurisdiction": chunk["jurisdiction"],
            "source_type": chunk["source_type"],
            "authority_level": chunk["authority_level"],
            "authority": chunk["authority"],
            "topic": chunk["topic"],
            "source_url": chunk["source_url"],
            "header": chunk["header"]
        })
        
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"[OK] Step 1 Corpus Ingestion Complete! Total indexed records in Chroma: {collection.count()}")
    return collection

if __name__ == "__main__":
    run_ingestion()
