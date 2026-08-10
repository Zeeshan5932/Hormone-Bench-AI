"""Offline batch job: run knowledge-graph entity/relation extraction over every document
already uploaded into data/documents/. Run after uploading papers, or periodically:

    python scripts/extract_kg.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.config import settings  # noqa: E402
from app.rag.document_loader import DocumentLoader  # noqa: E402
from app.services.kg_service import extract_and_store  # noqa: E402


def run() -> None:
    documents_dir = Path(settings.DOCUMENTS_DIR)
    if not documents_dir.exists():
        print(f"No documents directory found at {documents_dir}")
        return

    files = [f for f in documents_dir.iterdir() if f.suffix.lower() in {".pdf", ".docx", ".txt"}]
    if not files:
        print("No documents found to extract from.")
        return

    total_triples = 0
    for file_path in files:
        print(f"Extracting from {file_path.name}...")
        try:
            docs = DocumentLoader.load_file(str(file_path))
            full_text = "\n\n".join(d.page_content for d in docs)
            count = extract_and_store(full_text, source=file_path.name)
            total_triples += count
            print(f"  -> {count} triples extracted")
        except Exception as exc:
            print(f"  -> FAILED: {exc}")

    print(f"\nDone. {total_triples} total triples extracted from {len(files)} documents.")


if __name__ == "__main__":
    run()
