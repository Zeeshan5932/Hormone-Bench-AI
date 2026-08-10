"""Statistical Analysis Assistant: computes descriptive statistics, correlations, and outlier
counts from an uploaded CSV. Built standalone so it works before AI Developer 2's CSV
validation/schema-matching pipeline exists; its output is shaped as the same `DatasetSummary`
contract used by dataset_analysis_service, so their pipeline can plug into or replace this later
without changing any downstream code."""

from __future__ import annotations

import io
from typing import Any, Dict, List

import pandas as pd

from app.schemas.common import DatasetSummary
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger

# Common hormonal-health biomarker/feature names, flagged by a simple column-name heuristic.
KNOWN_BIOMARKERS = [
    "lh", "fsh", "amh", "tsh", "estrogen", "estradiol", "progesterone", "testosterone",
    "insulin", "glucose", "bmi", "cortisol", "prolactin", "shbg", "dhea", "hba1c",
]


class StatisticsError(AppBaseException):
    """Raised when a CSV cannot be parsed or analyzed."""


def _detect_features(columns: List[str]) -> List[str]:
    detected = []
    for col in columns:
        col_lower = col.lower()
        if any(biomarker in col_lower for biomarker in KNOWN_BIOMARKERS):
            detected.append(col)
    return detected


def _column_stats(series: pd.Series) -> Dict[str, Any]:
    missing_count = int(series.isna().sum())
    total = len(series)
    stats: Dict[str, Any] = {
        "name": str(series.name),
        "dtype": str(series.dtype),
        "missing_count": missing_count,
        "missing_pct": round(missing_count / total * 100, 2) if total else 0.0,
    }

    is_numeric = pd.api.types.is_numeric_dtype(series)

    if is_numeric:
        clean = series.dropna()
        stats["numeric"] = True
        if not clean.empty:
            q1, q3 = clean.quantile(0.25), clean.quantile(0.75)
            iqr = q3 - q1
            lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = clean[(clean < lower_bound) | (clean > upper_bound)]
            stats.update(
                {
                    "mean": round(float(clean.mean()), 4),
                    "median": round(float(clean.median()), 4),
                    "std": round(float(clean.std()), 4) if len(clean) > 1 else 0.0,
                    "min": round(float(clean.min()), 4),
                    "max": round(float(clean.max()), 4),
                    "q1": round(float(q1), 4),
                    "q3": round(float(q3), 4),
                    "outlier_count": int(len(outliers)),
                }
            )
    else:
        stats["numeric"] = False
        value_counts = series.value_counts().head(5)
        stats["unique_count"] = int(series.nunique(dropna=True))
        stats["top_values"] = {str(k): int(v) for k, v in value_counts.items()}

    return stats


def _correlation_matrix(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return {}

    corr = numeric_df.corr(numeric_only=True).round(4)
    return {col: corr[col].dropna().to_dict() for col in corr.columns}


def analyze_dataframe(df: pd.DataFrame, dataset_name: str = "uploaded_dataset") -> DatasetSummary:
    if df.empty:
        raise StatisticsError("The dataset is empty.")

    columns_stats = [_column_stats(df[col]) for col in df.columns]
    missing_value_summary = {
        col_stat["name"]: {"missing_count": col_stat["missing_count"], "missing_pct": col_stat["missing_pct"]}
        for col_stat in columns_stats
    }

    return DatasetSummary(
        dataset_name=dataset_name,
        row_count=len(df),
        column_count=len(df.columns),
        columns=columns_stats,
        missing_value_summary=missing_value_summary,
        detected_features=_detect_features(list(df.columns)),
        basic_stats={"correlations": _correlation_matrix(df)},
        notes=None,
    )


def analyze_csv_bytes(contents: bytes, dataset_name: str = "uploaded_dataset") -> DatasetSummary:
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        logger.exception("Failed to parse CSV: %s", exc)
        raise StatisticsError(f"Failed to parse CSV: {exc}") from exc

    return analyze_dataframe(df, dataset_name=dataset_name)
