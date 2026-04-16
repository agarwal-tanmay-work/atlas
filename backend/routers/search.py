from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import json

from config import GEMINI_API_KEY
from embeddings import embed_text
from database import search_by_embedding, get_failure_by_id, get_stats
from models.schemas import SearchResponse, SearchResult, FailureRecord

from google import genai

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY)

def _generate_cross_domain_insight(results: List[SearchResult]) -> Optional[str]:
    # Check if we have results from 2+ different domains
    domains = set(res.failure.domain for res in results)
    if len(domains) < 2:
        return None
    
    # Context building
    context = ""
    for r in results:
        context += f"- [{r.failure.domain}] {r.failure.title}: {r.failure.root_cause_category} ({r.failure.what_failed})\n"
        
    prompt = f"""
    You are a failure analyst. Look at these search results spanning multiple domains:
    {context}
    
    In exactly 2-3 sentences, identify the underlying pattern or structural similarity connecting these cross-domain failures.
    Be insightful and concise. Do not use markdown.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Insight generation failed: {e}")
        return None

def _perform_search(q: str, domain: Optional[str], root_cause: Optional[str], limit: int) -> SearchResponse:
    query_emb = embed_text(q)
    db_results = search_by_embedding(
        query_embedding=query_emb,
        n_results=limit,
        filter_domain=domain,
        filter_root_cause=root_cause
    )
    
    search_results = []
    for res in db_results:
        f_id = res["id"]
        distance = res.get("distance", 0)
        failure = get_failure_by_id(f_id)
        if failure:
            search_results.append(
                SearchResult(
                    failure=failure,
                    similarity_score=max(0, 1.0 - float(distance)),
                    match_reason="Semantic match based on failure descriptions"
                )
            )
            
    insight = _generate_cross_domain_insight(search_results)
    
    return SearchResponse(
        query=q,
        results=search_results,
        total=len(search_results),
        cross_domain_insight=insight
    )


@router.get("", response_model=SearchResponse)
def search_failures(
    q: str = Query(..., description="Semantic query"),
    domain: Optional[str] = None,
    root_cause: Optional[str] = None,
    limit: int = 10
):
    return _perform_search(q, domain, root_cause, limit)

@router.get("/by-symptom", response_model=SearchResponse)
def search_by_symptom(
    symptom: str = Query(..., description="Symptom to search for"),
    limit: int = 10
):
    augmented_query = f"failure symptom problem: {symptom}"
    return _perform_search(augmented_query, None, None, limit)

@router.get("/root-causes")
def get_root_causes():
    stats = get_stats()
    return stats.get("by_root_cause", {})

@router.get("/domains")
def get_domains():
    stats = get_stats()
    return stats.get("by_domain", {})
