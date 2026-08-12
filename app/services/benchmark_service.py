import pandas as pd
from app.schemas.dataset import QualityBenchmark

class BenchmarkService:
    @staticmethod
    def calculate_quality_benchmark(df: pd.DataFrame, anomalies_count: int = 0) -> QualityBenchmark:
        total_cells = df.size
        if total_cells == 0:
            return QualityBenchmark(completeness_score=0, uniqueness_score=0, validity_score=0, overall_quality_index=0)

        missing_cells = df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100.0

        duplicate_rows = df.duplicated().sum()
        total_rows = len(df)
        uniqueness = ((total_rows - duplicate_rows) / total_rows) * 100.0 if total_rows > 0 else 100.0

        validity = ((total_cells - anomalies_count) / total_cells) * 100.0 if total_cells > 0 else 100.0
        
        # Weighted Overall Quality Score
        overall_index = (0.4 * completeness) + (0.3 * uniqueness) + (0.3 * validity)

        return QualityBenchmark(
            completeness_score=round(completeness, 2),
            uniqueness_score=round(uniqueness, 2),
            validity_score=round(validity, 2),
            overall_quality_index=round(overall_index, 2)
        )