"""Research report generation: gather sources -> synthesize structured report -> attach citations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.llm.groq import get_llm
from app.prompts.loader import load_prompt
from app.services.citation_service import CitationStyle, format_citations
from app.services.research_service import research_service
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger

MAX_SOURCES = 12


class ReportGenerationError(AppBaseException):
    """Raised when a report cannot be assembled or generated."""


def _build_source_summaries(papers: List[Dict[str, Any]]) -> str:
    lines = []
    for idx, paper in enumerate(papers, start=1):
        abstract = (paper.get("abstract") or "No abstract available.").strip()
        authors = ", ".join(paper.get("authors") or []) or "Unknown authors"
        lines.append(
            f"[{idx}] {paper.get('title')} ({paper.get('year') or 'n.d.'}) - {authors}\n{abstract[:800]}"
        )
    return "\n\n".join(lines)


async def generate_report(
    topic: str,
    auto_search: bool = True,
    citation_style: CitationStyle = "apa",
) -> Dict[str, Any]:
    papers: List[Dict[str, Any]] = []

    if auto_search:
        papers = await research_service.search(topic, source="both", limit=MAX_SOURCES)

    if not papers:
        raise ReportGenerationError(f"No sources found for topic '{topic}'.")

    source_summaries = _build_source_summaries(papers)
    prompt_template = load_prompt("system/report_generator_v1.yaml")
    rendered = prompt_template.render(topic=topic, source_summaries=source_summaries)

    try:
        llm = get_llm()
        response = llm.invoke(rendered)
    except Exception as exc:
        logger.exception("Report generation failed: %s", exc)
        raise ReportGenerationError(f"Failed to generate report: {exc}") from exc

    references = format_citations(papers, citation_style)

    return {
        "markdown": response.content,
        "sources": papers,
        "references": references,
    }
