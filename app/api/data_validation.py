import io
import pandas as pd
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_validator_service import DataValidatorService
from app.services.benchmark_service import BenchmarkService
from app.services.explainability_service import ExplainabilityService

router = APIRouter()

@router.post("/dataset/process-and-validate")
async def process_and_validate_datasets(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
        
    dfs = []
    for file in files:
        filename = file.filename.lower()
        contents = await file.read()
        
        try:
            # Format-based parsing
            if filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(contents))
            elif filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(contents))
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file format: {file.filename}. Only CSV and Excel (.xlsx, .xls) are allowed."
                )
            dfs.append(df)
        except HTTPException:
            raise  # Re-raise HTTPExceptions as is
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading {file.filename}: {str(e)}")

    # Step 1: Merge Datasets (if multiple) & Clean schema
    merged_df = DataValidatorService.merge_and_standardize(dfs)

    # Step 2: Validate Data & Compute Quality Benchmark
    report = DataValidatorService.validate_biomarkers(merged_df)
    benchmark = BenchmarkService.calculate_quality_index(report)

    # Step 3: Get AI Recommendations
    prompt_vars = {
        "report": report.dict(),
        "quality_index": benchmark.overall_quality_index
    }
    suggestions = ExplainabilityService.generate_cleaning_suggestions(report.dict(), benchmark.overall_quality_index)

    return {
        "summary": report,
        "benchmark": benchmark,
        "recommendations": suggestions,
        "preview": merged_df.head(10).to_dict(orient="records")
    }