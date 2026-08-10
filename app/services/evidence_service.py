"""Evidence Summarizer: RAG + literature search -> a concise evidence card for a claim/topic."""

from __future__ import annotations

from typing import Any, Dict

from app.llm.groq import get_llm
from app.rag.retriever import DocumentRetriever
from app.rag.vectorstore import VectorStoreManager
from app.services.citation_service import format_citations
from app.services.research_service import research_service
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger

MAX_LITERATURE_SOURCES = 6
MAX_RAG_CHUNKS = 4


class EvidenceSummaryError(AppBaseException):
    """Raised when there is no evidence to summarize, or generation fails."""


async def summarize_evidence(topic_or_claim: str) -> Dict[str, Any]:
    papers = await research_service.search(topic_or_claim, source="both", limit=MAX_LITERATURE_SOURCES)

    vector_store_manager = VectorStoreManager()
    retriever = DocumentRetriever(vector_store_manager, k=MAX_RAG_CHUNKS)
    rag_docs = retriever.retrieve(topic_or_claim)

    evidence_pieces = []
    for idx, paper in enumerate(papers, start=1):
        abstract = (paper.get("abstract") or "").strip()
        evidence_pieces.append(f"[Lit {idx}] {paper.get('title')}: {abstract[:500]}")
    for idx, doc in enumerate(rag_docs, start=1):
        evidence_pieces.append(f"[Corpus {idx}] {doc.page_content[:500]}")

    if not evidence_pieces:
        raise EvidenceSummaryError(f"No supporting evidence found for '{topic_or_claim}'.")

    evidence_text = "\n\n".join(evidence_pieces)
    system_prompt = (
        "You are an evidence summarizer for hormonal health research. Using ONLY the evidence "
        "below, write a concise summary of what the evidence says about the claim/topic. "
        "Explicitly state the strength/limitations of the evidence (e.g. small sample sizes, "
        "single studies, conflicting results). If the evidence is insufficient, say so clearly.\n\n"
        f"Claim/topic: {topic_or_claim}\n\nEvidence:\n{evidence_text}"
    )

    try:
        llm = get_llm()
        response = llm.invoke(system_prompt)
    except Exception as exc:
        logger.exception("Evidence summarization failed: %s", exc)
        raise EvidenceSummaryError(f"Failed to summarize evidence: {exc}") from exc

    citations = format_citations(papers, "apa") if papers else []

    return {
        "claim": topic_or_claim,
        "summary": response.content,
        "supporting_sources": papers,
        "citations": citations,
    }
