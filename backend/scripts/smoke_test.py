"""End-to-end smoke test: hits every AI Developer 1 endpoint on a running server and reports
pass/fail per endpoint. Run the FastAPI server first (`uvicorn app.main:app`), then:

    python scripts/smoke_test.py

Set SKIP_LLM_TESTS=1 to skip endpoints that require a working GROQ_API_KEY/GOOGLE_API_KEY
(useful for a quick structural check before keys are configured).
"""

from __future__ import annotations

import os
import sys

import httpx

BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8000") + "/api/v1"
SKIP_LLM_TESTS = os.environ.get("SKIP_LLM_TESTS") == "1"

DUMMY_PAPER = {
    "id": "doi:10.1000/xyz123",
    "title": "Insulin Resistance and PCOS: A Review",
    "authors": ["Jane A Doe"],
    "year": 2021,
    "journal": "Journal of Endocrinology",
    "doi": "10.1000/xyz123",
    "source": "pubmed",
}

TESTS = [
    {"name": "health", "method": "GET", "path": "/health", "expect_keys": ["status", "model"]},
    {
        "name": "literature.search",
        "method": "GET",
        "path": "/literature/search",
        "params": {"q": "PCOS insulin resistance", "limit": 3},
        "expect_keys": ["papers"],
    },
    {
        "name": "citations.format (apa)",
        "method": "POST",
        "path": "/citations/format",
        "json": {"papers": [DUMMY_PAPER], "style": "apa"},
        "expect_keys": ["formatted"],
    },
    {
        "name": "citations.format (vancouver)",
        "method": "POST",
        "path": "/citations/format",
        "json": {"papers": [DUMMY_PAPER], "style": "vancouver"},
        "expect_keys": ["formatted"],
    },
    {
        "name": "citations.format (bibtex)",
        "method": "POST",
        "path": "/citations/format",
        "json": {"papers": [DUMMY_PAPER], "style": "bibtex"},
        "expect_keys": ["formatted"],
    },
    {
        "name": "search.semantic",
        "method": "GET",
        "path": "/search/semantic",
        "params": {"q": "hormone", "top_k": 3},
        "expect_keys": ["results"],
    },
    {
        "name": "papers.summarize",
        "method": "POST",
        "path": "/papers/summarize",
        "json": {"text": "Estrogen and progesterone regulate the menstrual cycle. This paper reviews their interaction with the hypothalamic-pituitary-gonadal axis in a cohort of 200 participants, finding significant correlation between hormone levels and cycle length."},
        "expect_keys": ["background", "key_findings"],
        "requires_llm": True,
    },
    {
        "name": "dataset-analysis.interpret",
        "method": "POST",
        "path": "/dataset-analysis/interpret",
        "json": {"dataset_summary": {"dataset_name": "demo", "row_count": 100, "columns": [], "detected_features": ["LH", "FSH", "BMI"]}},
        "expect_keys": ["interpretation"],
        "requires_llm": True,
    },
    {
        "name": "tutor.explain",
        "method": "POST",
        "path": "/tutor/explain",
        "json": {"topic": "PCOS", "level": "beginner"},
        "expect_keys": ["explanation"],
        "requires_llm": True,
    },
    {
        "name": "tutor.quiz",
        "method": "POST",
        "path": "/tutor/quiz",
        "json": {"topic": "PCOS", "num_questions": 2, "difficulty": "easy"},
        "expect_keys": ["questions"],
        "requires_llm": True,
    },
    {
        "name": "tutor.flashcards",
        "method": "POST",
        "path": "/tutor/flashcards",
        "json": {"topic": "PCOS", "count": 2},
        "expect_keys": ["cards"],
        "requires_llm": True,
    },
    {
        "name": "tutor.notes",
        "method": "POST",
        "path": "/tutor/notes",
        "json": {"topic": "PCOS"},
        "expect_keys": ["notes_markdown"],
        "requires_llm": True,
    },
    {
        "name": "education.ask",
        "method": "POST",
        "path": "/education/ask",
        "json": {"question": "What is estrogen?"},
        "expect_keys": ["answer", "disclaimer"],
        "requires_llm": True,
    },
    {
        "name": "evidence.summarize",
        "method": "POST",
        "path": "/evidence/summarize",
        "json": {"topic_or_claim": "metformin and PCOS"},
        "expect_keys": ["summary", "citations"],
        "requires_llm": True,
    },
    {
        "name": "reports.generate",
        "method": "POST",
        "path": "/reports/generate",
        "json": {"topic": "PCOS and insulin resistance", "auto_search": True},
        "expect_keys": ["markdown", "references"],
        "requires_llm": True,
    },
    {
        "name": "chat",
        "method": "POST",
        "path": "/chat",
        "json": {"message": "Hello, what can you help me with?"},
        "expect_keys": ["answer", "route_used"],
        "requires_llm": True,
    },
    {
        "name": "kg.extract",
        "method": "POST",
        "path": "/kg/extract",
        "json": {"text": "Insulin resistance is strongly associated with PCOS. Elevated LH/FSH ratio is an indicator of PCOS.", "source": "smoke_test"},
        "expect_keys": ["triples_extracted"],
        "requires_llm": True,
    },
    {
        "name": "kg.entity",
        "method": "GET",
        "path": "/kg/entity/PCOS",
        "expect_keys": ["entity", "relations"],
        "requires_llm": True,
    },
    {
        "name": "kg.ask",
        "method": "POST",
        "path": "/kg/ask",
        "json": {"question": "What is PCOS associated with?"},
        "expect_keys": ["answer", "facts_used"],
        "requires_llm": True,
    },
]

# Statistics endpoints take a CSV file upload rather than JSON, so they're tested separately
# below (skipped in the requires_llm-free run since /analyze/full calls the LLM).
STATISTICS_SAMPLE_CSV = (
    b"patient_id,age,bmi,lh,fsh,diagnosis\n"
    b"1,25,22.5,5.1,6.2,control\n"
    b"2,29,31.2,12.4,4.1,PCOS\n"
    b"3,31,27.8,9.8,5.0,PCOS\n"
)


def run() -> int:
    passed, failed, skipped = 0, 0, 0

    with httpx.Client(timeout=60.0) as client:
        for test in TESTS:
            if test.get("requires_llm") and SKIP_LLM_TESTS:
                print(f"SKIP  {test['name']} (requires_llm, SKIP_LLM_TESTS=1)")
                skipped += 1
                continue

            try:
                if test["method"] == "GET":
                    resp = client.get(BASE_URL + test["path"], params=test.get("params"))
                else:
                    resp = client.post(BASE_URL + test["path"], json=test.get("json"))

                if resp.status_code >= 400:
                    print(f"FAIL  {test['name']} -> HTTP {resp.status_code}: {resp.text[:200]}")
                    failed += 1
                    continue

                body = resp.json()
                missing = [k for k in test.get("expect_keys", []) if k not in body]
                if missing:
                    print(f"FAIL  {test['name']} -> missing keys {missing} in response")
                    failed += 1
                    continue

                print(f"PASS  {test['name']}")
                passed += 1

            except Exception as exc:
                print(f"FAIL  {test['name']} -> {exc}")
                failed += 1

        # File-upload endpoints, tested separately since they take multipart form data.
        upload_tests = [
            {"name": "statistics.analyze", "path": "/statistics/analyze", "expect_keys": ["row_count", "columns"], "requires_llm": False},
            {"name": "statistics.analyze.full", "path": "/statistics/analyze/full", "expect_keys": ["dataset_summary", "interpretation"], "requires_llm": True},
        ]
        for test in upload_tests:
            if test["requires_llm"] and SKIP_LLM_TESTS:
                print(f"SKIP  {test['name']} (requires_llm, SKIP_LLM_TESTS=1)")
                skipped += 1
                continue
            try:
                files = {"file": ("sample.csv", STATISTICS_SAMPLE_CSV, "text/csv")}
                resp = client.post(BASE_URL + test["path"], files=files)

                if resp.status_code >= 400:
                    print(f"FAIL  {test['name']} -> HTTP {resp.status_code}: {resp.text[:200]}")
                    failed += 1
                    continue

                body = resp.json()
                missing = [k for k in test["expect_keys"] if k not in body]
                if missing:
                    print(f"FAIL  {test['name']} -> missing keys {missing} in response")
                    failed += 1
                    continue

                print(f"PASS  {test['name']}")
                passed += 1
            except Exception as exc:
                print(f"FAIL  {test['name']} -> {exc}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
