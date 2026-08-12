import pandas as pd
from typing import List, Dict, Tuple, Any
from app.schemas.dataset import DatasetValidationReport
from app.services.schema_matcher import SchemaMatcher

BIOMARKER_BOUNDS = {
    "fsh": (0.0, 200.0),
    "lh": (0.0, 200.0),
    "estrogen": (0.0, 2000.0),
    "progesterone": (0.0, 100.0),
    "glucose": (30.0, 600.0),
    "bmi": (10.0, 80.0)
}

class DataValidatorService:
    def __init__(self):
        self.matcher = SchemaMatcher()

    def merge_datasets(self, dataframes: List[pd.DataFrame], join_type: str = "outer") -> pd.DataFrame:
        if not dataframes:
            return pd.DataFrame()
        
        base_df = dataframes[0]
        for next_df in dataframes[1:]:
            common_keys = list(set(base_df.columns).intersection(set(next_df.columns)))
            if common_keys:
                base_df = pd.merge(base_df, next_df, on=common_keys[0], how=join_type)
            else:
                base_df = pd.concat([base_df, next_df], axis=0, ignore_index=True)
        return base_df

    def validate_dataset(self, df: pd.DataFrame) -> Tuple[DatasetValidationReport, int]:
        total_rows, total_cols = df.shape
        missing_cells = int(df.isnull().sum().sum())
        missing_pct = float((missing_cells / df.size) * 100) if df.size > 0 else 0.0
        duplicates = int(df.duplicated().sum())

        missing_per_col = {col: int(val) for col, val in df.isnull().sum().items()}
        col_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

        anomalies: Dict[str, List[Dict[str, Any]]] = {}
        total_anomalies_count = 0

        for col in df.columns:
            col_lower = col.lower()
            for key, (min_val, max_val) in BIOMARKER_BOUNDS.items():
                if key in col_lower and pd.api.types.is_numeric_dtype(df[col]):
                    invalid_mask = (df[col] < min_val) | (df[col] > max_val)
                    invalid_rows = df[invalid_mask]
                    if not invalid_rows.empty:
                        anomalies[col] = [
                            {"row": int(idx), "value": float(val), "reason": f"Out of physiological range ({min_val}-{max_val})"}
                            for idx, val in invalid_rows[col].items()
                        ]
                        total_anomalies_count += len(invalid_rows)

        report = DatasetValidationReport(
            total_rows=total_rows,
            total_columns=total_cols,
            missing_cells=missing_cells,
            missing_percentage=round(missing_pct, 2),
            duplicate_rows=duplicates,
            column_types=col_types,
            missing_per_column=missing_per_col,
            biomarker_anomalies=anomalies
        )
        return report, total_anomalies_count