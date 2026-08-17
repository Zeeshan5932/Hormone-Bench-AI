"""Statistical Analysis Assistant endpoints: compute descriptive statistics from an uploaded
CSV, with an optional AI-generated narrative interpretation layered on top."""

from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from backend.app.schemas.common import DatasetSummary
from backend.app.services.dataset_analysis_service import DatasetAnalysisError, interpret_dataset
from backend.app.services.statistics_service import StatisticsError, analyze_csv_bytes

router = APIRouter(prefix="/statistics", tags=["statistics"])


class StatisticalAnalysisResponse(BaseModel):
    dataset_summary: DatasetSummary
    interpretation: str


def _require_csv(filename: str) -> None:
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .csv files are supported.")


@router.post("/analyze", response_model=DatasetSummary)
async def analyze_csv(file: UploadFile = File(...)):
    """Pure computed statistics — no LLM call, fast and deterministic."""
    _require_csv(file.filename)
    try:
        contents = await file.read()
        return analyze_csv_bytes(contents, dataset_name=file.filename)
    except StatisticsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/analyze/full", response_model=StatisticalAnalysisResponse)
async def analyze_csv_full(file: UploadFile = File(...)):
    """Computed statistics plus an AI-generated narrative interpretation, reusing the same
    dataset_analysis_service used for AI Developer 2's future validated output."""
    _require_csv(file.filename)
    try:
        contents = await file.read()
        summary = analyze_csv_bytes(contents, dataset_name=file.filename)
    except StatisticsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    try:
        interpretation = interpret_dataset(summary.model_dump())
    except DatasetAnalysisError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return StatisticalAnalysisResponse(dataset_summary=summary, interpretation=interpretation)
