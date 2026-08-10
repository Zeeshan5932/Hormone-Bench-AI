"""Deterministic citation formatters (APA, Vancouver, BibTeX) — no LLM involved, to avoid
citation hallucination. Reused by both the citations endpoint and the report generator."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Literal

CitationStyle = Literal["apa", "vancouver", "bibtex"]


def _format_authors_apa(authors: List[str]) -> str:
    """'Jane Doe' -> 'Doe, J.'; APA 7th: '&' before the last author, '...' beyond 20 authors."""

    def to_apa(name: str) -> str:
        parts = name.strip().split()
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        last = parts[-1]
        initials = " ".join(f"{p[0]}." for p in parts[:-1] if p)
        return f"{last}, {initials}"

    formatted = [a for a in (to_apa(name) for name in authors) if a]
    if not formatted:
        return ""
    if len(formatted) == 1:
        return formatted[0]
    if len(formatted) <= 20:
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"
    return ", ".join(formatted[:19]) + ", ... " + formatted[-1]


def _format_authors_vancouver(authors: List[str]) -> str:
    """'Jane Doe' -> 'Doe J'; list up to 6 authors, 'et al' beyond that."""

    def to_vancouver(name: str) -> str:
        parts = name.strip().split()
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        last = parts[-1]
        initials = "".join(p[0] for p in parts[:-1] if p)
        return f"{last} {initials}"

    formatted = [a for a in (to_vancouver(name) for name in authors) if a]
    if not formatted:
        return ""
    if len(formatted) > 6:
        return ", ".join(formatted[:6]) + ", et al"
    return ", ".join(formatted)


def format_apa(paper: Dict[str, Any]) -> str:
    authors = _format_authors_apa(paper.get("authors") or [])
    year = paper.get("year")
    year_str = f"({year})" if year else "(n.d.)"
    title = (paper.get("title") or "Untitled").rstrip(".")
    journal = paper.get("journal")
    doi = paper.get("doi")
    url = paper.get("url")

    citation = f"{authors} {year_str}." if authors else f"{year_str}."
    citation += f" {title}."
    if journal:
        citation += f" {journal}."
    if doi:
        citation += f" https://doi.org/{doi}"
    elif url:
        citation += f" {url}"
    return citation.strip()


def format_vancouver(paper: Dict[str, Any]) -> str:
    authors = _format_authors_vancouver(paper.get("authors") or [])
    title = (paper.get("title") or "Untitled").rstrip(".")
    journal = paper.get("journal")
    year = paper.get("year")
    doi = paper.get("doi")

    citation = f"{authors}. " if authors else ""
    citation += f"{title}."
    if journal:
        citation += f" {journal}."
    if year:
        citation += f" {year}."
    if doi:
        citation += f" doi:{doi}"
    return citation.strip()


def _bibtex_key(paper: Dict[str, Any]) -> str:
    authors = paper.get("authors") or []
    first_author_last = authors[0].split()[-1] if authors and authors[0].split() else "unknown"
    year = paper.get("year") or "nd"
    title_words = (paper.get("title") or "untitled").split()
    title_word = re.sub(r"[^a-zA-Z0-9]", "", title_words[0]) if title_words else "untitled"
    key = f"{first_author_last}{year}{title_word}".lower()
    return re.sub(r"[^a-z0-9]", "", key) or "untitled"


def format_bibtex(paper: Dict[str, Any]) -> str:
    key = _bibtex_key(paper)
    authors = " and ".join(paper.get("authors") or [])
    fields = {
        "title": paper.get("title") or "Untitled",
        "author": authors,
        "year": str(paper.get("year")) if paper.get("year") else "",
        "journal": paper.get("journal") or "",
        "doi": paper.get("doi") or "",
        "url": paper.get("url") or "",
    }
    non_empty = [(name, value) for name, value in fields.items() if value]

    lines = [f"@article{{{key},"]
    for idx, (field_name, value) in enumerate(non_empty):
        escaped = value.replace("{", "").replace("}", "")
        trailing_comma = "," if idx < len(non_empty) - 1 else ""
        lines.append(f"  {field_name} = {{{escaped}}}{trailing_comma}")
    lines.append("}")
    return "\n".join(lines)


_FORMATTERS = {
    "apa": format_apa,
    "vancouver": format_vancouver,
    "bibtex": format_bibtex,
}


def format_citation(paper: Dict[str, Any], style: CitationStyle) -> str:
    formatter = _FORMATTERS.get(style)
    if not formatter:
        raise ValueError(f"Unsupported citation style: {style}")
    return formatter(paper)


def format_citations(papers: List[Dict[str, Any]], style: CitationStyle) -> List[str]:
    return [format_citation(paper, style) for paper in papers]
