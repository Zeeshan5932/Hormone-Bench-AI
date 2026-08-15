"""Biomedical Knowledge Graph Q&A endpoints (lightweight SQLite + NetworkX)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.services.kg_service import KnowledgeGraphError, ask, extract_and_store, get_entity

router = APIRouter(prefix="/kg", tags=["knowledge-graph"])


class KGExtractRequest(BaseModel):
    text: str
    source: Optional[str] = None


class KGExtractResponse(BaseModel):
    triples_extracted: int


class KGEntityResponse(BaseModel):
    entity: str
    relations: List[Dict[str, Any]]


class KGAskRequest(BaseModel):
    question: str


class KGAskResponse(BaseModel):
    answer: str
    facts_used: List[str]


@router.post("/extract", response_model=KGExtractResponse, status_code=status.HTTP_201_CREATED)
async def extract_endpoint(request: KGExtractRequest):
    try:
        count = extract_and_store(request.text, source=request.source)
    except KnowledgeGraphError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    return KGExtractResponse(triples_extracted=count)


@router.get("/entity/{name}", response_model=KGEntityResponse)
async def entity_endpoint(name: str):
    result = get_entity(name)
    return KGEntityResponse(**result)


@router.post("/ask", response_model=KGAskResponse)
async def ask_endpoint(request: KGAskRequest):
    try:
        result = await ask(request.question)
    except KnowledgeGraphError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return KGAskResponse(**result)
