"""Student AI Tutor: explain / quiz / flashcards / notes. Shares its underlying LLM-call
pattern with the Hormone Education Agent (education_service.py)."""

from __future__ import annotations

from backend.app.llm.groq import get_llm
from backend.app.prompts.loader import load_prompt
from backend.app.schemas.tutor import FlashcardSet, Quiz
from backend.app.utils.exceptions import AppBaseException
from backend.app.utils.logger import logger


class TutorError(AppBaseException):
    """Raised when a tutor generation call fails."""


def explain_topic(topic: str, level: str = "beginner") -> str:
    prompt_template = load_prompt("system/student_tutor_v1.yaml")
    system_prompt = prompt_template.render(topic=topic, level=level)
    instruction = f"Explain the topic '{topic}' at a {level} level in a few clear paragraphs."

    try:
        llm = get_llm()
        response = llm.invoke(f"{system_prompt}\n\n{instruction}")
        return response.content
    except Exception as exc:
        logger.exception("Tutor explain failed: %s", exc)
        raise TutorError(f"Failed to generate explanation: {exc}") from exc


def generate_quiz(topic: str, num_questions: int = 5, difficulty: str = "medium") -> Quiz:
    prompt_template = load_prompt("tasks/generate_quiz_v1.yaml")
    rendered = prompt_template.render(topic=topic, num_questions=num_questions, difficulty=difficulty)

    try:
        structured_llm = get_llm().with_structured_output(Quiz)
        return structured_llm.invoke(rendered)
    except Exception as exc:
        logger.exception("Quiz generation failed: %s", exc)
        raise TutorError(f"Failed to generate quiz: {exc}") from exc


def generate_flashcards(topic: str, count: int = 10) -> FlashcardSet:
    instruction = (
        f"Generate {count} flashcards for studying '{topic}' in the context of hormonal health. "
        "Return ONLY a JSON object with key 'cards', a list of objects with keys 'front' and 'back'."
    )
    try:
        structured_llm = get_llm().with_structured_output(FlashcardSet)
        return structured_llm.invoke(instruction)
    except Exception as exc:
        logger.exception("Flashcard generation failed: %s", exc)
        raise TutorError(f"Failed to generate flashcards: {exc}") from exc


def generate_notes(topic: str) -> str:
    instruction = (
        f"Write structured study notes (Markdown, with headings and bullet points) on '{topic}' "
        "in the context of hormonal health, suitable for a student reviewing for an exam."
    )
    try:
        llm = get_llm()
        response = llm.invoke(instruction)
        return response.content
    except Exception as exc:
        logger.exception("Notes generation failed: %s", exc)
        raise TutorError(f"Failed to generate notes: {exc}") from exc
