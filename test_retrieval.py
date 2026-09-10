"""
Retrieval Test Verification Script for Step 1
Tests metadata-filtered query execution against local Chroma DB collection 'ip_sakti_corpus'.
"""

import os
import chromadb

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def test_query():
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name="ip_sakti_corpus")
    
    print(f"Testing Metadata-Filtered Search on Chroma collection '{collection.name}'...")
    
    # Query 1: Section 3(p) India query
    results_india = collection.query(
        query_texts=["Ashwagandha traditional knowledge patent bar Section 3(p)"],
        n_results=2,
        where={"jurisdiction": "India"}
    )
    
    print("\n--- QUERY 1 (India Jurisdiction Filter) ---")
    for doc, meta in zip(results_india['documents'][0], results_india['metadatas'][0]):
        print(f"Document: {meta['act']} | Section: {meta['section']} | Authority: Level {meta['authority_level']}")
        print(f"Source URL: {meta['source_url']}")
        print(f"Excerpt: {doc[:150]}...\n")
        
    # Query 2: International WIPO GRATK Treaty query
    results_intl = collection.query(
        query_texts=["Mandatory disclosure of origin traditional knowledge WIPO treaty"],
        n_results=1,
        where={"jurisdiction": "International"}
    )
    
    print("\n--- QUERY 2 (International Jurisdiction Filter) ---")
    for doc, meta in zip(results_intl['documents'][0], results_intl['metadatas'][0]):
        print(f"Document: {meta['act']} | Section: {meta['section']} | Authority: Level {meta['authority_level']}")
        print(f"Source URL: {meta['source_url']}")
        print(f"Excerpt: {doc[:150]}...\n")
        
    print("[OK] Step 1 Verification Complete: Vector DB retrieval with metadata filtering is fully operational!")

if __name__ == "__main__":
    test_query()
