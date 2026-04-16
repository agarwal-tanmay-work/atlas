"""
Seed data ingestion pipeline.

Ingests the hardcoded seed failures from seed_data.py into PostgreSQL with pgvector embeddings.
Run this FIRST, then run ingest_danluu.py to add the Dan Luu post-mortems.
"""

import sys
import os
import hashlib

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, insert_failure, failure_exists, update_related_failures, get_all_failures, search_by_embedding
from embeddings import embed_failure
from models.schemas import FailureRecord
from ingestion.seed_data import get_seed_failures

def generate_deterministic_id(title: str) -> str:
    return hashlib.md5(title.encode('utf-8')).hexdigest()

def run():
    print("Initializing database...")
    init_db()

    raw_failures = get_seed_failures()
    total = len(raw_failures)
    
    print(f"Starting ingestion of {total} seed failures...")
    
    inserted_count = 0
    domains = {}
    
    # 1 & 2: Insert into PostgreSQL with embeddings
    for i, raw_fail in enumerate(raw_failures):
        fail_id = generate_deterministic_id(raw_fail["title"])
        
        if failure_exists(fail_id):
            print(f"Skipping duplicate: {raw_fail['title']}")
            if raw_fail["domain"] not in domains:
                domains[raw_fail["domain"]] = 0
            domains[raw_fail["domain"]] += 1
            continue
            
        record_data = raw_fail.copy()
        record_data["id"] = fail_id
        record_data["related_failure_ids"] = []
        
        record = FailureRecord(**record_data)
        
        # Embed
        embedding = embed_failure(record)
        
        # Store in PostgreSQL (with embedding)
        insert_failure(record, embedding)
        
        inserted_count += 1
        
        # Track stats
        if record.domain not in domains:
            domains[record.domain] = 0
        domains[record.domain] += 1
        
        print(f"Inserted {inserted_count} of {total} failures... ({record.title})")
        
    # 3: Relationship Engine
    print("\nRunning relationship engine to map cross-domain connectivity...")
    all_db_failures = get_all_failures(limit=1000)
    for i, failure in enumerate(all_db_failures):
        embedding = embed_failure(failure)
        
        # Search for top 6 (including self)
        results = search_by_embedding(embedding, n_results=6)
        
        related_ids = []
        for res in results:
            if res["id"] != failure.id:
                related_ids.append(res["id"])
                
        # Limit to top 5
        related_ids = related_ids[:5]
        
        update_related_failures(failure.id, related_ids)
        print(f"Mapped {len(related_ids)} related incidents for {failure.title}")

    print("\n=== INGESTION COMPLETE ===")
    print(f"Total newly inserted: {inserted_count}")
    print("Domain breakdown:")
    for key, val in domains.items():
        print(f"  - {key}: {val}")

if __name__ == "__main__":
    run()
