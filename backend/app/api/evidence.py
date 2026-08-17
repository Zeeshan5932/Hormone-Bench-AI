"""Evidence Summarizer endpoint."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.schemas.common import Paper
from backend.app.services.evidence_service import EvidenceSummaryError, summarize_evidence

router = APIRouter(prefix="/evidence", tags=["evidence"])


class EvidenceSummarizeRequest(BaseModel):
    topic_or_claim: str


class EvidenceSummarizeResponse(BaseModel):
    claim: str
    summary: str
    supporting_sources: List[Paper]
    citations: List[str]


@router.post("/summarize", response_model=EvidenceSummarizeResponse)
async def summarize_evidence_endpoint(request: EvidenceSummarizeRequest):
    try:
        result = await summarize_evidence(request.topic_or_claim)
    except EvidenceSummaryError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return EvidenceSummarizeResponse(
        claim=result["claim"],
        summary=result["summary"],
        supporting_sources=[Paper(**p) for p in result["supporting_sources"]],
        citations=result["citations"],
    )
