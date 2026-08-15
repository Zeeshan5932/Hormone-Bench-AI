"""Semantic Scholar Graph API client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from backend.app.config import settings
from backend.app.utils.logger import logger

S2_BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,abstract,year,authors,externalIds,venue,citationCount,url"


class SemanticScholarClient:
    """Thin wrapper over the Semantic Scholar Graph API. Works without an API key at a lower rate limit."""

    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.api_key = settings.SEMANTIC_SCHOLAR_API_KEY

    def _headers(self) -> Dict[str, str]:
        return {"x-api-key": self.api_key} if self.api_key else {}

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout, headers=self._headers()) as client:
            try:
                resp = await client.get(
                    f"{S2_BASE}/paper/search",
                    params={"query": query, "limit": limit, "fields": FIELDS},
                )
                resp.raise_for_status()
            except Exception as exc:
                logger.error("Semantic Scholar search failed: %s", exc)
                return []

        data = resp.json().get("data", [])
        return [self._normalize(item) for item in data]

    async def fetch_by_id(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """paper_id: a Semantic Scholar id, or a prefixed external id, e.g. 'DOI:10.1000/xyz'."""
        async with httpx.AsyncClient(timeout=self.timeout, headers=self._headers()) as client:
            try:
                resp = await client.get(f"{S2_BASE}/paper/{paper_id}", params={"fields": FIELDS})
                resp.raise_for_status()
            except Exception as exc:
                logger.error("Semantic Scholar fetch_by_id failed: %s", exc)
                return None

        return self._normalize(resp.json())

    def _normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        external_ids = item.get("externalIds") or {}
        doi = external_ids.get("DOI")
        pmid = external_ids.get("PubMed")
        authors = [a.get("name", "") for a in (item.get("authors") or []) if a.get("name")]

        return {
            "id": f"doi:{doi}" if doi else f"s2:{item.get('paperId')}",
            "title": item.get("title") or "Untitled",
            "authors": authors,
            "year": item.get("year"),
            "journal": item.get("venue") or None,
            "abstract": item.get("abstract"),
            "doi": doi,
            "pmid": pmid,
            "url": item.get("url"),
            "source": "semantic_scholar",
            "citation_count": item.get("citationCount"),
        }
