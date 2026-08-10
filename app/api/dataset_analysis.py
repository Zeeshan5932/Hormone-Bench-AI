"""Dataset analysis endpoint: narrative interpretation over AI Developer 2's validated dataset stats."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.common import DatasetSummary
from app.services.dataset_analysis_service import DatasetAnalysisError, interpret_dataset

router = APIRouter(prefix="/dataset-analysis", tags=["dataset-analysis"])


class DatasetInterpretRequest(BaseModel):
    dataset_summary: DatasetSummary


class DatasetInterpretResponse(BaseModel):
    interpretation: str


@router.post("/interpret", response_model=DatasetInterpretResponse)
async def interpret_dataset_endpoint(request: DatasetInterpretRequest):
    try:
        interpretation = interpret_dataset(request.dataset_summary.model_dump())
    except DatasetAnalysisError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return DatasetInterpretResponse(interpretation=interpretation)
