"""Citation formatting endpoint: deterministic APA / Vancouver / BibTeX generation."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.schemas.common import Paper
from backend.app.services.citation_service import CitationStyle, format_citations

router = APIRouter(prefix="/citations", tags=["citations"])


class CitationFormatRequest(BaseModel):
    papers: List[Paper]
    style: CitationStyle = "apa"


class CitationFormatResponse(BaseModel):
    formatted: List[str]


@router.post("/format", response_model=CitationFormatResponse)
async def format_citations_endpoint(request: CitationFormatRequest):
    papers = [p.model_dump() for p in request.papers]
    formatted = format_citations(papers, request.style)
    return CitationFormatResponse(formatted=formatted)
