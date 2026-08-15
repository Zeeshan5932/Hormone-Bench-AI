"""Dataset analysis narrative: interprets AI Developer 2's structured dataset summary via LLM.
Does not re-validate the dataset — that responsibility belongs to AI Developer 2's pipeline."""

from __future__ import annotations

import json
from typing import Any, Dict

from backend.app.llm.groq import get_llm
from backend.app.prompts.loader import load_prompt
from backend.app.utils.exceptions import AppBaseException
from backend.app.utils.logger import logger


class DatasetAnalysisError(AppBaseException):
    """Raised when the LLM narrative over a dataset summary cannot be generated."""


def interpret_dataset(dataset_summary: Dict[str, Any]) -> str:
    prompt_template = load_prompt("tasks/interpret_dataset_v1.yaml")
    rendered = prompt_template.render(dataset_summary=json.dumps(dataset_summary, indent=2, default=str))

    try:
        llm = get_llm()
        response = llm.invoke(rendered)
        return response.content
    except Exception as exc:
        logger.exception("Dataset interpretation failed: %s", exc)
        raise DatasetAnalysisError(f"Failed to interpret dataset: {exc}") from exc
