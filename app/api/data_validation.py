from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io

from app.services.data_validator_service import DataValidatorService
from app.services.benchmark_service import BenchmarkService
from app.services.explainability_service import ExplainabilityService

router = APIRouter(prefix="/dataset", tags=["Data Validation & Engineering"])
validator = DataValidatorService()

@router.post("/process-and-validate")
async def process_and_validate_csvs(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    
    dfs = []
    for file in files:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        dfs.append(df)

    merged_df = validator.merge_datasets(dfs)
    report, anomalies_count = validator.validate_dataset(merged_df)
    benchmark = BenchmarkService.calculate_quality_benchmark(merged_df, anomalies_count)
    suggestions = ExplainabilityService.generate_cleaning_suggestions(report.dict(), benchmark.overall_quality_index)

    return {
        "validation_report": report,
        "quality_benchmark": benchmark,
        "cleaning_suggestions": suggestions
    }