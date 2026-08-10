"""Paper summarization: DOI/PMID lookup or raw text -> structured summary via LLM."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.llm.groq import get_llm
from app.prompts.loader import load_prompt
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger

MAX_CHARS = 40000  # guard against unusually long documents blowing the context window


class PaperSummary(BaseModel):
    background: str = Field(description="Background and motivation for the study.")
    methods: str = Field(description="Study design and methodology.")
    key_findings: str = Field(description="The main results.")
    limitations: str = Field(description="Stated or apparent limitations.")
    relevance_to_hormonal_health: str = Field(description="How this relates to hormonal health research.")
    plain_language_summary: str = Field(description="A summary a non-expert could understand.")


class SummarizationError(AppBaseException):
    """Raised when a paper cannot be fetched or summarized."""


def summarize_text(text: str) -> PaperSummary:
    if not text.strip():
        raise SummarizationError("No text provided to summarize.")

    prompt_template = load_prompt("tasks/summarize_paper_v1.yaml")
    rendered = prompt_template.render(paper_text=text[:MAX_CHARS])

    try:
        structured_llm = get_llm().with_structured_output(PaperSummary)
        return structured_llm.invoke(rendered)
    except Exception as exc:
        logger.exception("Paper summarization failed: %s", exc)
        raise SummarizationError(f"Failed to summarize paper: {exc}") from exc


async def summarize_paper(
    *, doi: Optional[str] = None, pmid: Optional[str] = None, text: Optional[str] = None
) -> PaperSummary:
    """Summarize by DOI/PMID lookup or raw text. File uploads are resolved to text by the caller."""
    if text:
        return summarize_text(text)

    if doi or pmid:
        from app.services.research_service import research_service  # local import: avoid a module-load cycle

        paper = await research_service.fetch_paper(doi=doi, pmid=pmid)
        if not paper or not paper.get("abstract"):
            raise SummarizationError("Could not fetch an abstract for the given doi/pmid.")
        return summarize_text(paper["abstract"])

    raise SummarizationError("Provide doi, pmid, or text.")
