"""Shared Pydantic models reused across literature, citation, report, and evidence endpoints."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Paper(BaseModel):
    """Normalized paper metadata, regardless of whether it came from PubMed or Semantic Scholar."""

    id: str = Field(description="Stable identifier: DOI if available, otherwise source-prefixed id (e.g. 'pmid:12345').")
    title: str
    authors: List[str] = Field(default_factory=list)
    year: Optional[int] = None
    journal: Optional[str] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    source: str = Field(description="'pubmed' or 'semantic_scholar'")
    citation_count: Optional[int] = None


class SourceRef(BaseModel):
    """A single retrieval source backing a generated answer (RAG chunk, web result, or paper)."""

    source: str
    url: Optional[str] = ""
    page: Optional[int] = None
    snippet: Optional[str] = None


class Citation(BaseModel):
    """A normalized citation record, ready to be formatted by the citation service."""

    url: Optional[str] = ""
    source: str = ""
    page: Optional[int] = None


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    detail: Optional[Any] = None


class DatasetSummary(BaseModel):
    """Provisional shape for the structured dataset summary handed off by AI Developer 2's
    validation pipeline. Treat as a draft contract until confirmed against their real output."""

    dataset_name: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    columns: List[Dict[str, Any]] = Field(default_factory=list)
    missing_value_summary: Dict[str, Any] = Field(default_factory=dict)
    detected_features: List[str] = Field(default_factory=list)
    basic_stats: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None
