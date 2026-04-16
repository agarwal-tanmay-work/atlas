from pydantic import BaseModel
from typing import Optional, List


class FailureRecord(BaseModel):
    id: str
    title: str
    domain: str  # e.g. "Software Engineering", "Aviation", "Finance"
    subdomain: Optional[str] = None  # e.g. "Database", "Deployment", "Banking"
    year: Optional[int] = None
    organization: Optional[str] = None
    what_failed: str  # 1-2 sentence summary of what broke
    root_cause: str  # The underlying cause
    root_cause_category: str  # One of the universal categories
    warning_signs: List[str]  # Bullet list of ignored signals
    what_was_done_wrong: str
    how_it_was_fixed: Optional[str] = None
    lesson: str  # The single most important takeaway
    severity: str  # "Low", "Medium", "High", "Critical"
    source_url: Optional[str] = None
    tags: List[str]
    related_failure_ids: List[str] = []  # IDs of similar failures across domains


class SearchResult(BaseModel):
    failure: FailureRecord
    similarity_score: float
    match_reason: str


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int
    cross_domain_insight: Optional[str] = None


class AnalyzeRequest(BaseModel):
    project_description: str


class AnalyzeResponse(BaseModel):
    project_description: str
    risk_summary: str
    top_analogous_failures: List[FailureRecord]
    most_likely_root_causes: List[str]
    warning_signs_to_watch: List[str]
    recommended_mitigations: List[str]
    overall_risk_level: str  # "Low", "Medium", "High", "Critical"
