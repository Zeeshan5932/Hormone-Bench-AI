"""Standalone semantic search over the ingested RAG corpus (retrieval only, no generation)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.app.rag.retriever import DocumentRetriever
from backend.app.rag.vectorstore import VectorStoreManager

router = APIRouter(prefix="/search", tags=["search"])


class SemanticSearchResult(BaseModel):
    content: str
    source: str
    page: Optional[int] = None
    score: Optional[float] = None


class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult]


@router.get("/semantic", response_model=SemanticSearchResponse)
async def semantic_search(q: str = Query(..., min_length=1), top_k: int = Query(10, ge=1, le=50)):
    vector_store_manager = VectorStoreManager()
    retriever = DocumentRetriever(vector_store_manager, k=top_k)
    scored_docs = retriever.retrieve_with_scores(q)

    results = [
        SemanticSearchResult(
            content=doc.page_content,
            source=doc.metadata.get("source_file") or doc.metadata.get("source") or "unknown",
            page=doc.metadata.get("page"),
            score=float(score),
        )
        for doc, score in scored_docs
    ]
    return SemanticSearchResponse(results=results)
