"""Hormone Education Agent endpoint: public Q&A with mandatory medical disclaimer."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.services.education_service import EducationError, answer_question

router = APIRouter(prefix="/education", tags=["education"])


class EducationAskRequest(BaseModel):
    question: str


class EducationAskResponse(BaseModel):
    answer: str
    disclaimer: str
    related_resources: List[str] = []


@router.post("/ask", response_model=EducationAskResponse)
async def ask_endpoint(request: EducationAskRequest):
    try:
        result = answer_question(request.question)
    except EducationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return EducationAskResponse(answer=result["answer"], disclaimer=result["disclaimer"], related_resources=[])
