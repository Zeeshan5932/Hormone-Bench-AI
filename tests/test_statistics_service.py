"""Unit tests for the Statistical Analysis Assistant's pure-computation path (no LLM/API keys)."""

import pandas as pd
import pytest

from app.services.statistics_service import StatisticsError, analyze_csv_bytes, analyze_dataframe

SAMPLE_CSV = b"""patient_id,age,bmi,lh,fsh,diagnosis
1,25,22.5,5.1,6.2,control
2,29,31.2,12.4,4.1,PCOS
3,,27.8,9.8,5.0,PCOS
4,34,21.0,4.9,6.5,control
5,41,29.9,,4.8,PCOS
"""


def test_analyze_csv_bytes_basic_shape():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    assert summary.dataset_name == "sample"
    assert summary.row_count == 5
    assert summary.column_count == 6


def test_detects_hormonal_biomarker_columns():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    assert "bmi" in summary.detected_features
    assert "lh" in summary.detected_features
    assert "fsh" in summary.detected_features
    assert "patient_id" not in summary.detected_features


def test_missing_value_summary_counts_nulls():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    age_missing = summary.missing_value_summary["age"]
    assert age_missing["missing_count"] == 1
    lh_missing = summary.missing_value_summary["lh"]
    assert lh_missing["missing_count"] == 1


def test_numeric_column_gets_descriptive_stats():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    bmi_col = next(c for c in summary.columns if c["name"] == "bmi")
    assert bmi_col["numeric"] is True
    assert "mean" in bmi_col
    assert "outlier_count" in bmi_col


def test_categorical_column_gets_value_counts():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    diagnosis_col = next(c for c in summary.columns if c["name"] == "diagnosis")
    assert diagnosis_col["numeric"] is False
    assert diagnosis_col["top_values"]["PCOS"] == 3
    assert diagnosis_col["top_values"]["control"] == 2


def test_correlation_matrix_present_for_multiple_numeric_columns():
    summary = analyze_csv_bytes(SAMPLE_CSV, dataset_name="sample")
    correlations = summary.basic_stats["correlations"]
    assert "bmi" in correlations
    assert "lh" in correlations["bmi"]


def test_empty_dataframe_raises_statistics_error():
    with pytest.raises(StatisticsError):
        analyze_dataframe(pd.DataFrame())


def test_malformed_csv_raises_statistics_error():
    with pytest.raises(StatisticsError):
        analyze_csv_bytes(b"\x00\x01not,a,valid\xffcsv", dataset_name="broken")
