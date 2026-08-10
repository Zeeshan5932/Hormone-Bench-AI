"""Literature search + ingestion orchestration (PubMed + Semantic Scholar -> RAG corpus)."""

from __future__ import annotations

import asyncio
import re
from typing import Any, Dict, List, Literal, Optional

from langchain_core.documents import Document

from app.rag.chunker import DocumentChunker
from app.rag.vectorstore import VectorStoreManager
from app.services.pubmed_client import PubMedClient
from app.services.semantic_scholar_client import SemanticScholarClient
from app.utils.cache import TTLCache
from app.utils.logger import logger

_search_cache = TTLCache(ttl_seconds=3600)


def _normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def _dedupe_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Dedupe by DOI first, falling back to normalized title for papers with no DOI."""
    seen_dois: set = set()
    seen_titles: set = set()
    deduped: List[Dict[str, Any]] = []

    for paper in papers:
        doi_key = (paper.get("doi") or "").lower()
        title_key = _normalize_title(paper.get("title", ""))

        if doi_key and doi_key in seen_dois:
            continue
        if not doi_key and title_key in seen_titles:
            continue

        if doi_key:
            seen_dois.add(doi_key)
        seen_titles.add(title_key)
        deduped.append(paper)

    return deduped


class ResearchService:
    """Orchestrates external literature search and ingestion into the shared RAG corpus."""

    def __init__(self):
        self.pubmed = PubMedClient()
        self.semantic_scholar = SemanticScholarClient()
        self.chunker = DocumentChunker(chunk_size=800, chunk_overlap=100)
        self.vector_store_manager = VectorStoreManager(collection_name="documents")

    async def search(
        self,
        query: str,
        source: Literal["pubmed", "semantic_scholar", "both"] = "both",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        cache_key = f"lit:{source}:{limit}:{query.strip().lower()}"
        cached = _search_cache.get(cache_key)
        if cached is not None:
            logger.info("Literature search cache hit for '%s'", query)
            return cached

        tasks = []
        if source in ("pubmed", "both"):
            tasks.append(self.pubmed.search(query, limit=limit))
        if source in ("semantic_scholar", "both"):
            tasks.append(self.semantic_scholar.search(query, limit=limit))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        papers: List[Dict[str, Any]] = []
        for result in results:
            if isinstance(result, BaseException):
                logger.error("Literature source failed: %s", result)
                continue
            papers.extend(result)

        deduped = _dedupe_papers(papers)[:limit]
        _search_cache.set(cache_key, deduped)
        return deduped

    async def fetch_paper(self, doi: Optional[str] = None, pmid: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch full normalized metadata (incl. abstract) for a single paper by DOI or PMID."""
        if pmid:
            paper = await self.pubmed.fetch_by_pmid(pmid)
            if paper and paper.get("abstract"):
                return paper
        if doi:
            paper = await self.semantic_scholar.fetch_by_id(f"DOI:{doi}")
            if paper:
                return paper
        return None

    def ingest_paper(self, paper: Dict[str, Any]) -> int:
        """Chunk a paper's abstract and upsert it into the shared Chroma RAG corpus. Returns chunk count."""
        text = (paper.get("abstract") or "").strip()
        if not text:
            return 0

        doc = Document(
            page_content=text,
            metadata={
                "source_file": paper.get("title", "unknown"),
                "source": "literature",
                "paper_id": paper.get("id"),
                "doi": paper.get("doi") or "",
                "pmid": paper.get("pmid") or "",
                "year": paper.get("year") or 0,
                "page": 1,
            },
        )
        chunks = self.chunker.split_documents([doc])
        indexed_ids = self.vector_store_manager.add_documents(chunks)
        return len(indexed_ids)


research_service = ResearchService()
