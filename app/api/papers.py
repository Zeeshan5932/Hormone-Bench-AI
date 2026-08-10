"""Paper summarization endpoints: DOI/PMID/raw text, or an uploaded PDF/DOCX/TXT file."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.rag.document_loader import DocumentLoader
from app.services.summarizer_service import PaperSummary, SummarizationError, summarize_paper, summarize_text
from app.utils.logger import logger

router = APIRouter(prefix="/papers", tags=["papers"])


class PaperSummarizeRequest(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None
    text: Optional[str] = None


@router.post("/summarize", response_model=PaperSummary)
async def summarize_paper_endpoint(request: PaperSummarizeRequest):
    if not (request.doi or request.pmid or request.text):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide doi, pmid, or text.")

    try:
        return await summarize_paper(doi=request.doi, pmid=request.pmid, text=request.text)
    except SummarizationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.post("/summarize/upload", response_model=PaperSummary)
async def summarize_uploaded_paper(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx", ".txt"}
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '{file_ext}'. Allowed: {allowed_extensions}",
        )

    tmp_path: Optional[Path] = None
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(contents)
            tmp_path = Path(tmp.name)

        docs = DocumentLoader.load_file(str(tmp_path))
        full_text = "\n\n".join(doc.page_content for doc in docs)
        return summarize_text(full_text)
    except SummarizationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Failed to summarize uploaded file: %s", exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    finally:
        if tmp_path and tmp_path.exists():
            os.remove(tmp_path)
