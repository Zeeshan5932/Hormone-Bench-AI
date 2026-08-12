from app.prompts.loader import render_prompt
from app.services.gemini_client import generate_response # Uses shared LLM utility from Role 1

class ExplainabilityService:
    @staticmethod
    def generate_cleaning_suggestions(report_dict: dict, quality_index: float) -> str:
        prompt_vars = {
            "total_rows": report_dict.get("total_rows"),
            "total_columns": report_dict.get("total_columns"),
            "missing_percentage": report_dict.get("missing_percentage"),
            "duplicate_rows": report_dict.get("duplicate_rows"),
            "quality_index": quality_index,
            "missing_per_column": report_dict.get("missing_per_column"),
            "anomalies": report_dict.get("biomarker_anomalies")
        }
        
        prompt = render_prompt("tasks/data_cleaning.yaml", prompt_vars)
        response = generate_response(prompt)
        return response