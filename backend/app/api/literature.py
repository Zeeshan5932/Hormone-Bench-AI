"""Literature search endpoints: external PubMed/Semantic Scholar search + RAG ingestion."""

from __future__ import annotations

from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from backend.app.schemas.common import Paper
from backend.app.services.research_service import research_service

router = APIRouter(prefix="/literature", tags=["literature"])


class LiteratureSearchResponse(BaseModel):
    papers: List[Paper]


class LiteratureIngestRequest(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None


class LiteratureIngestResponse(BaseModel):
    paper_id: str
    chunks_ingested: int


@router.get("/search", response_model=LiteratureSearchResponse)
async def search_literature(
    q: str = Query(..., min_length=1),
    source: Literal["pubmed", "semantic_scholar", "both"] = "both",
    limit: int = Query(20, ge=1, le=50),
):
    papers = await research_service.search(q, source=source, limit=limit)
    return LiteratureSearchResponse(papers=[Paper(**p) for p in papers])


@router.post("/ingest", response_model=LiteratureIngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_literature(request: LiteratureIngestRequest):
    if not request.doi and not request.pmid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide a doi or pmid.")

    paper = await research_service.fetch_paper(doi=request.doi, pmid=request.pmid)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found or has no abstract available to ingest.",
        )

    chunks_ingested = research_service.ingest_paper(paper)
    return LiteratureIngestResponse(paper_id=paper["id"], chunks_ingested=chunks_ingested)
