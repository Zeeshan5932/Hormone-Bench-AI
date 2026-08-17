"""NCBI E-utilities client for PubMed literature search."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

import httpx

from backend.app.config import settings
from backend.app.utils.logger import logger

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


class PubMedClient:
    """Thin wrapper over esearch + efetch. Works without an API key at a lower rate limit."""

    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.api_key = settings.NCBI_API_KEY

    def _params(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"db": "pubmed", **extra}
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search PubMed and return normalized paper dicts."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                esearch_resp = await client.get(
                    f"{EUTILS_BASE}/esearch.fcgi",
                    params=self._params(term=query, retmax=limit, sort="relevance", retmode="json"),
                )
                esearch_resp.raise_for_status()
                pmids = esearch_resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as exc:
                logger.error("PubMed esearch failed: %s", exc)
                return []

            if not pmids:
                return []

            try:
                efetch_resp = await client.get(
                    f"{EUTILS_BASE}/efetch.fcgi",
                    params=self._params(id=",".join(pmids), retmode="xml", rettype="abstract"),
                )
                efetch_resp.raise_for_status()
            except Exception as exc:
                logger.error("PubMed efetch failed: %s", exc)
                return []

        return self._parse_efetch_xml(efetch_resp.text)

    async def fetch_by_pmid(self, pmid: str) -> Optional[Dict[str, Any]]:
        """Fetch full normalized metadata (incl. abstract) for a single PMID."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(
                    f"{EUTILS_BASE}/efetch.fcgi",
                    params=self._params(id=pmid, retmode="xml", rettype="abstract"),
                )
                resp.raise_for_status()
            except Exception as exc:
                logger.error("PubMed fetch_by_pmid failed: %s", exc)
                return None

        papers = self._parse_efetch_xml(resp.text)
        return papers[0] if papers else None

    def _parse_efetch_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        papers: List[Dict[str, Any]] = []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            logger.error("Failed to parse PubMed XML: %s", exc)
            return papers

        for article in root.findall(".//PubmedArticle"):
            try:
                medline = article.find("MedlineCitation")
                pmid = medline.findtext("PMID", default="")
                article_el = medline.find("Article")
                title = (article_el.findtext("ArticleTitle") or "").strip()

                abstract_parts = [node.text or "" for node in article_el.findall("Abstract/AbstractText")]
                abstract = " ".join(part.strip() for part in abstract_parts if part).strip() or None

                authors: List[str] = []
                for author in article_el.findall("AuthorList/Author"):
                    last = author.findtext("LastName")
                    fore = author.findtext("ForeName")
                    if last and fore:
                        authors.append(f"{fore} {last}")
                    elif last:
                        authors.append(last)

                journal = article_el.findtext("Journal/Title")
                year_text = article_el.findtext("Journal/JournalIssue/PubDate/Year")
                year = int(year_text) if year_text and year_text.isdigit() else None

                doi = None
                for eid in article.findall(".//ArticleId"):
                    if eid.get("IdType") == "doi":
                        doi = eid.text

                papers.append(
                    {
                        "id": f"doi:{doi}" if doi else f"pmid:{pmid}",
                        "title": title or "Untitled",
                        "authors": authors,
                        "year": year,
                        "journal": journal,
                        "abstract": abstract,
                        "doi": doi,
                        "pmid": pmid,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
                        "source": "pubmed",
                        "citation_count": None,
                    }
                )
            except Exception as exc:
                logger.warning("Skipping malformed PubMed record: %s", exc)
                continue

        return papers
