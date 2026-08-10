"""Hormone Education Agent: public-facing Q&A with mandatory medical disclaimer guardrails.
Shares its underlying LLM-call pattern with the Student Tutor (tutor_service.py)."""

from __future__ import annotations

from typing import Any, Dict

from app.llm.groq import get_llm
from app.prompts.loader import apply_medical_guardrails, load_medical_disclaimer, load_prompt
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger


class EducationError(AppBaseException):
    """Raised when the education agent fails to produce an answer."""


def answer_question(question: str) -> Dict[str, Any]:
    prompt_template = load_prompt("system/hormone_education_v1.yaml")
    system_prompt = apply_medical_guardrails(prompt_template.render(question=question))

    try:
        llm = get_llm()
        response = llm.invoke(system_prompt)
    except Exception as exc:
        logger.exception("Hormone education Q&A failed: %s", exc)
        raise EducationError(f"Failed to answer question: {exc}") from exc

    return {
        "answer": response.content,
        "disclaimer": load_medical_disclaimer(),
    }
