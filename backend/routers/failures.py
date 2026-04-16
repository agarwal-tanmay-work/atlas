from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from database import get_all_failures, get_failure_by_id, get_stats
from models.schemas import FailureRecord

router = APIRouter()


@router.get("/stats")
def get_failure_stats():
    return get_stats()


@router.get("", response_model=List[FailureRecord])
def get_failures_list(
    domain: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    return get_all_failures(domain=domain, severity=severity, limit=limit, offset=offset)


@router.get("/{failure_id}")
def get_failure(failure_id: str):
    record = get_failure_by_id(failure_id)
    if not record:
        raise HTTPException(status_code=404, detail="Failure not found")

    related = []
    for rel_id in record.related_failure_ids:
        r = get_failure_by_id(rel_id)
        if r:
            related.append(r)

    return {
        "failure": record,
        "related_failures": related,
    }
