"""Research report generation endpoint."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.common import Paper
from app.services.citation_service import CitationStyle
from app.services.report_service import ReportGenerationError, generate_report

router = APIRouter(prefix="/reports", tags=["reports"])


class ReportGenerateRequest(BaseModel):
    topic: str
    auto_search: bool = True
    citation_style: CitationStyle = "apa"


class ReportGenerateResponse(BaseModel):
    markdown: str
    sources: List[Paper]
    references: List[str]


@router.post("/generate", response_model=ReportGenerateResponse)
async def generate_report_endpoint(request: ReportGenerateRequest):
    try:
        result = await generate_report(
            topic=request.topic,
            auto_search=request.auto_search,
            citation_style=request.citation_style,
        )
    except ReportGenerationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return ReportGenerateResponse(
        markdown=result["markdown"],
        sources=[Paper(**p) for p in result["sources"]],
        references=result["references"],
    )
