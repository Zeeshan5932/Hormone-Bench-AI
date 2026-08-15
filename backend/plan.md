# HormoneBench AI — AI Developer 1 Development Plan

## Context

HormoneBench AI is a 16-day hackathon project: an AI-powered research ecosystem for women's
hormonal health (Research Hub, Student Academy, Patient Awareness Center, Healthcare
Professional Portal), built by a 7-person team (Founder/PM, Full Stack Developer, AI Developer 1,
AI Developer 2, Researcher 1, Researcher 2, Business/FinTech Expert) on Next.js + FastAPI +
Google Gemini.

The user is filling the **AI Developer 1 ("Research AI Engineer")** role. Per the team's planning
docs, this role owns Gemini integration, the Research Copilot, literature search, RAG, semantic
search, citation generation, research report generation, and (per the broader ecosystem doc) the
Student AI Tutor and Hormone Education Agent. Deliverables: Research Agent, Paper Search,
Dataset Analysis, Evidence Summarizer, Research Reports.

No codebase exists in the working directory yet — only 4 planning PDFs. The user will clone the
team's shared repo separately and reconcile it against this plan to see what AI Developer 1's slice
already has vs. what's missing. This plan is therefore the **target-state design and 16-day build
plan** for that role, meant to be diffed against reality once the repo is cloned.

**Confirmed technology choices** (user decisions):
- Vector store: **ChromaDB** (local, free, fast to stand up)
- Literature search sources: **PubMed/NCBI E-utilities + Semantic Scholar API** (both free)
- Service layout (mounted into shared FastAPI backend vs. standalone microservice): **undecided
  until the repo is cloned** — the codebase below is built to work either way with zero code
  changes, and step 1 of the build order below is resolving this with whatever's already in the
  Full Stack Developer's code.

## Module/Folder Structure

A self-contained Python package, portable between "mounted into the shared FastAPI app" and
"run standalone":

```
research_ai/
├── main.py                    # standalone entrypoint: uvicorn research_ai.main:app
├── app_factory.py             # create_app(); get_routers() -> [(router, prefix, tags)]
├── config.py                  # pydantic Settings: GEMINI_API_KEY, NCBI_API_KEY, S2_API_KEY, CHROMA_PATH
├── routers/                   # thin HTTP layer
│   ├── health.py  copilot.py  literature.py  papers.py  search.py
│   ├── citations.py  reports.py  dataset_analysis.py  evidence.py
│   └── tutor.py  education.py  knowledge_graph.py
├── services/                  # business logic, no HTTP concerns
│   ├── gemini_client.py       # generate(), generate_json(), embed(), stream()
│   ├── pubmed_client.py       # NCBI E-utilities wrapper
│   ├── semantic_scholar_client.py
│   ├── chroma_store.py        # collection mgmt, upsert, query
│   ├── pdf_ingest.py          # PDF/text extraction + chunking
│   ├── copilot_service.py     # chat orchestration: retrieval routing + generation
│   ├── literature_service.py  # search + merge/dedupe + normalize
│   ├── summarizer_service.py  # paper summarization
│   ├── rag_service.py         # embed -> retrieve -> context -> generate
│   ├── citation_service.py    # deterministic APA/Vancouver/BibTeX formatters
│   ├── report_service.py      # report assembly pipeline
│   ├── dataset_analysis_service.py  # Gemini narrative over AI Dev2's validated stats
│   ├── tutor_service.py  education_service.py
│   ├── kg_service.py          # entity/relation extraction + NetworkX query
│   └── session_store.py       # SQLite-backed conversation memory
├── prompts/                   # the "Prompt Library" (Founder-owned deliverable, AI Dev1-fed)
│   ├── loader.py               # Jinja2-templated, versioned prompt rendering
│   └── library/{system,tasks,guardrails}/*.yaml, CHANGELOG.md
├── schemas/                   # pydantic request/response models (common.py, chat.py, literature.py, reports.py, tutor.py)
├── core/                      # exceptions.py, logging.py, cache.py, retry.py
├── data/{chroma/, seed_corpus/}
├── scripts/                   # ingest_corpus.py, extract_kg.py, smoke_test.py
└── tests/                     # unit + mocked-integration tests
```

**Portability mechanism:** no router/service imports a global `app` object. Gemini/Chroma/config
clients are provided via FastAPI `Depends()`. `main.py` calls `create_app()` for standalone runs;
the Full Stack Developer can instead import `get_routers()` and `include_router()` them into the
shared backend under `/api/ai/*`. Confirm which mode with the team first.

## Core Feature Specs

**Research Copilot** (core, the demo spine): session-based chat (`session_store.py`, SQLite).
Message handling in `copilot_service.py`: cheap intent routing (literature-search vs. RAG-answer),
RAG retrieval from Chroma, grounded generation with inline citation markers, explicit "insufficient
evidence" fallback instead of inventing citations. Keep tool selection rule-based/deterministic for
reliability; native Gemini function-calling is a stretch upgrade only if time allows after the core path is stable.

**Literature Search** (core): `literature_service.py` queries PubMed E-utilities (`esearch`→
`esummary`/`efetch`) and Semantic Scholar Graph API in parallel, dedupes by DOI, normalizes into
a shared `Paper` schema. Register both free API keys immediately to raise rate limits. Cache results
(~1hr TTL) to protect the live demo from API flakiness.

**Paper Summarization** (core): DOI/PMID/raw-text/PDF input → structured JSON output
(background, methods, key findings, limitations, relevance, plain-language summary) via Gemini
JSON mode. Map-reduce only for unusually long docs (>40-50 pages).

**RAG Pipeline** (core, backbone): chunk ingested papers (~500-800 tokens, ~100 overlap, keep
`paper_id/title/authors/year/section` metadata) → embed with Gemini embeddings → store in a
single Chroma `research_corpus` collection (disposable/reproducible — never source of truth) →
retrieve top_k≈5-8 on query → generate with a "answer only from provided context, cite
inline" system prompt.

**Semantic Search** (core, cheap once Chroma exists): thin wrapper querying the ingested corpus
directly, no generation.

**Citation Generator** (core): deterministic formatters (not LLM-generated, to avoid citation
hallucination) for APA + Vancouver (biomedical standard) + BibTeX, unit-tested against edge cases
(missing authors/DOI, >6-author "et al." rules). Reused by both Copilot and Report Generator.

**Research Report Generator** (core): gather sources (literature search + RAG, capped ~10-15) →
per-source summaries → one structured Gemini call producing standard sections (Executive
Summary, Background, Literature Review, Key Findings, Discussion, Limitations, Conclusion,
References) → citation_service builds reference list → output both Markdown and structured JSON.

**Dataset Analysis / Evidence Summarizer** (core, cross-team dependency): consumes a structured
JSON dataset summary produced by **AI Developer 2's** validation pipeline (do not redo
validation/schema-matching) and generates a Gemini narrative interpretation, optionally enriched
with related literature. Draft a provisional JSON contract using mocked data early so this isn't
blocked waiting on AI Dev2; confirm the real shape once the repo is cloned. Evidence Summarizer
(`/evidence/summarize`) is a closely related sibling: RAG + literature search → evidence card with
claim, supporting sources, strength caveat, citations.

**Student AI Tutor & Hormone Education Agent** (core): build as one shared persona-toggle
implementation. Tutor: explain/quiz/flashcards/study-notes endpoints with structured JSON output.
Education Agent: public Q&A with **mandatory medical disclaimer** and "when to seek care"
framing. Ideal grounding is Researcher 2's curated content (once available); core path can ship on
well-crafted prompts + guardrails alone.

**Knowledge Graph Q&A** (stretch, pragmatic-lite): skip Neo4j — disproportionate effort for 16
days. Instead: offline Gemini-based entity/relation triple extraction over the ingested corpus →
store in SQLite → load into NetworkX for 1-2 hop traversal → `/kg/ask` extracts entities from a
question, traverses for facts, feeds facts (+RAG) to Gemini for a grounded answer. First feature to
cut if behind schedule.

## API Contract (endpoints AI Developer 1 owns)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health`, `/version` | liveness |
| POST | `/copilot/sessions` | start chat session |
| POST | `/copilot/sessions/{id}/messages` | send chat message → `{reply, sources[], citations[]}` |
| GET | `/copilot/sessions/{id}` | chat history |
| GET | `/literature/search?q=&source=&limit=` | external paper search |
| POST | `/literature/ingest {doi\|pmid}` | pull paper into RAG corpus |
| POST | `/papers/summarize` | summarize one paper |
| GET | `/search/semantic?q=&top_k=` | search ingested corpus only |
| POST | `/citations/format {papers[], style}` | APA/Vancouver/BibTeX |
| POST | `/reports/generate {topic, auto_search?}` | full research report |
| POST | `/dataset-analysis/interpret {dataset_summary}` | narrative over AI Dev2's stats |
| POST | `/evidence/summarize {topic_or_claim}` | evidence card |
| POST | `/tutor/explain`, `/tutor/quiz`, `/tutor/flashcards`, `/tutor/notes` | Student Tutor |
| POST | `/education/ask {question}` | public Hormone Education Q&A |
| GET | `/kg/entity/{name}`, POST `/kg/ask {question}` | graph Q&A (stretch) |

Shared `ErrorResponse {error_code, message, detail?}` across all endpoints for the frontend's error
handling.

## Prompt Library

Versioned YAML templates under `prompts/library/{system,tasks,guardrails}/`, rendered via a
single Jinja2 `loader.py` code path (no service builds prompt strings by hand). Centralize the
medical disclaimer text and a `apply_medical_guardrails()` helper applied to every patient/public-
facing persona. Draft the guardrail text early and hand to the Founder for sign-off (it's formally
the Founder's "Prompt Library" deliverable, but AI Dev1 needs it immediately). Version via filename
suffix (`_v1`, `_v2`) + git history + a lightweight `CHANGELOG.md` — no heavier tooling needed for
16 days. Test prompts with pytest: template rendering, guardrail-phrase presence checks, and
structured-output schema validation.

## Build Order (single session, no day-splitting)

Everything below is being built in one continuous push rather than spread across 16 days. Order
matters — each step unblocks the next, so build top to bottom:

1. Clone repo, reconcile against this plan (see "Next Steps"), resolve mount-vs-standalone with
   whatever Full Stack code already exists. Scaffold package, `app_factory`, config, `/health`.
2. Get/confirm Gemini + NCBI + Semantic Scholar API keys in `.env`.
3. Prompt library skeleton + loader + medical disclaimer guardrail text.
4. PubMed + Semantic Scholar clients, normalized `Paper` schema, mocked tests.
5. Literature search endpoint end-to-end.
6. `chroma_store.py` + `pdf_ingest.py` (chunking).
7. Research Copilot v1: sessions + plain (non-RAG) chat, `Citation`/`SourceRef` schemas.
8. RAG ingestion pipeline: Gemini embeddings + Chroma upsert; ingest seed references.
9. Wire RAG into Copilot → grounded, cited answers. Paper summarization endpoint.
10. Citation Generator (APA/Vancouver/BibTeX, unit-tested).
11. Research Report Generator (reuses summarizer + citation service).
12. Dataset Analysis + Evidence Summarizer (against the draft/mocked AI Dev2 contract).
13. Student AI Tutor + Hormone Education Agent (shared persona pattern).
14. Knowledge Graph Q&A — only if everything above is solid and stable (first thing to cut).
15. Frontend integration pass: confirm contracts, CORS, error shapes with whatever frontend exists.
16. Test everything end-to-end (`smoke_test.py`, `/docs`), fix, then freeze.

## Testing / Verification

- FastAPI's built-in `/docs` Swagger UI as the daily manual-test surface (works standalone or mounted).
- A checked-in `.http`/Postman collection exercising every endpoint, so teammates can test integration without reading the AI code.
- `scripts/smoke_test.py` — httpx script hitting every endpoint, asserting response shape; run before pushing and as the final testing gate.
- pytest: fast unit tests for deterministic logic (citation formatting, chunking, prompt rendering) + mocked tests for Gemini/PubMed/Semantic Scholar clients (no API cost). A few `@pytest.mark.integration` tests hit real APIs, run manually, skipped by default.
- For LLM outputs: validate structure (pydantic schema) and required elements (citation markers, disclaimer text) rather than exact-string matching, since generation is non-deterministic.
- Test each feature standalone via `/docs` before wiring into Copilot orchestration.

## Risks & Mitigations

- **Gemini cost/rate limits** → use Flash for high-volume tasks, cap `max_output_tokens`, cache during dev, handle rate-limit errors gracefully.
- **Medical hallucination risk** → strict context-only RAG prompting, always-attached citations, mandatory disclaimers on patient-facing agents, explicit "insufficient evidence" fallback, route sampled outputs through Researcher 1's review.
- **PubMed/Semantic Scholar rate limits/downtime on demo day** → register API keys early, cache + backoff (tenacity), **pre-warm caches for the exact demo queries**, degrade to RAG-only corpus if live search fails.
- **Prompt injection via ingested papers** → treat ingested text as data not instructions; verify disclaimer presence on medical-topic outputs before returning.
- **Chroma fragility** → pin version, keep ingestion idempotent/reproducible so the store is fully disposable.
- **Solo-dev bandwidth** → explicit cut order if running out of time: (1) drop Knowledge Graph, (2) fold Education Agent into Tutor's shared code path, (3) keep Dataset Analysis (cheap, core), (4) never cut Copilot + RAG + Literature Search + Citations + Report Generator.
- **Cross-team dependencies** (AI Dev2's dataset JSON contract, Researcher 2's content, Researcher 1's sign-off) → draft contracts early with mocked data so this role isn't blocked waiting on others.

## Next Steps

1. Clone the team's shared repo.
2. Diff its current state against this plan's folder structure and endpoint list to find what's already built vs. missing.
3. Resolve the mount-vs-standalone decision with the Full Stack Developer (step 1 above).
4. Confirm the real dataset-analysis JSON contract with AI Developer 2.
5. Start executing the build order, top to bottom, in one continuous session.

## Build Status (reconciled against the cloned repo)

The cloned repo (`RAGentic AI`) turned out to be a standalone FastAPI + LangGraph + Streamlit app
— not a shared Next.js monorepo — so the "standalone" mode applies: `app/` is the AI Developer 1
service on its own, mounted at `/api/v1`. Generation uses **Groq Llama 3.3** (kept, by team
decision) with **Gemini** used for embeddings only.

**Already built pre-session:** RAG pipeline (`app/rag/`), LangGraph-based Research Copilot
(`app/agents/`, `app/services/chat_service.py`), document upload/ingestion, web search + URL
reader tools (bonus, beyond plan scope), a minimal Streamlit frontend (later removed — see below).

**Built this session (on top of the above):**
- Prompt library (`app/prompts/library/**`) + Jinja2 loader + medical disclaimer guardrail
- Literature search: `app/services/pubmed_client.py`, `semantic_scholar_client.py`,
  `research_service.py` → `/literature/search`, `/literature/ingest`
- Real citation generator (APA/Vancouver/BibTeX, unit-tested) → `/citations/format`
- Paper summarizer (DOI/PMID/text/upload) → `/papers/summarize`, `/papers/summarize/upload`
- Semantic-search-only endpoint → `/search/semantic`
- Research report generator → `/reports/generate`
- Dataset analysis + evidence summarizer → `/dataset-analysis/interpret`, `/evidence/summarize`
  (dataset contract is still a provisional draft — confirm against AI Dev2's real output)
- Student Tutor + Hormone Education Agent (shared pattern, guardrails applied) →
  `/tutor/explain|quiz|flashcards|notes`, `/education/ask`
- SQLite-backed session persistence (`langgraph-checkpoint-sqlite`) replacing in-memory `MemorySaver`
- Biomedical Knowledge Graph Q&A: `app/services/kg_service.py` (SQLite + NetworkX, not a full
  graph DB — deliberate scope call for a hackathon-sized corpus) → `/kg/extract`, `/kg/entity/{name}`,
  `/kg/ask`, plus `scripts/extract_kg.py` for offline batch extraction over uploaded documents.
  Initially miscategorized as "stretch" in this plan's first draft; the Team Structure PDF lists
  Knowledge Graph as one of AI Developer 1's explicit core responsibilities, so it was built, not cut.
- Fixed a pre-existing gap in `requirements.txt` (`langchain-chroma` was imported by
  `app/rag/vectorstore.py` but never listed) and a stale path in `run.py` (originally pointed at a
  nonexistent `app/ui/app.py`)
- Statistical Analysis Assistant: `app/services/statistics_service.py` computes real descriptive
  stats/correlations/outliers/hormonal-biomarker detection from an uploaded CSV via pandas →
  `/statistics/analyze` (pure stats, no LLM) and `/statistics/analyze/full` (stats + AI narrative,
  reusing `dataset_analysis_service`). AI Developer 2 hadn't started their CSV/validation pipeline
  yet, so this was built standalone rather than left as a gap — its output is shaped as the same
  `DatasetSummary` contract, so their real pipeline can plug into or replace it later without
  changing `/dataset-analysis/interpret` or anything downstream.
- `tests/test_citation_service.py`, `tests/test_prompts_render.py`, `tests/test_statistics_service.py`,
  `scripts/smoke_test.py`

**Verified live, end-to-end, with real Groq + Gemini keys:** all 21 endpoints in
`scripts/smoke_test.py` pass against a running server — literature search, all 3 citation styles,
paper summarization, semantic search, dataset analysis, tutor (explain/quiz/flashcards/notes),
education Q&A, evidence summarizer, report generation, the original chat endpoint, knowledge graph
extract/entity/ask, and both statistics endpoints (tested with a real CSV upload). 27/27 pytest
unit tests also pass.

## Frontend cleanup + test dashboard

The pre-existing minimal Streamlit frontend (`frontend/streamlit_app.py`,
`frontend/components/{chat,sidebar,sources}.py`) only called `/chat` and `/documents/upload` — it
had no idea about any of the 15+ endpoints built this session, and wasn't AI Developer 1's
responsibility anyway (that's the Full Stack Developer's Next.js build, per the Team Structure
PDF). It was removed entirely to avoid confusion.

In its place: **`frontend/test_dashboard.py`** — a single-file, 13-tab Streamlit dashboard
covering every endpoint (Chat, Upload, Literature, Summarize, Citations, Semantic Search, Reports,
Dataset Analysis, Statistics, Evidence, Tutor, Education, Knowledge Graph). Verified with
Streamlit's headless `AppTest` harness — zero exceptions, all tabs render. This is a testing tool,
not a production frontend. `run.py` was updated to launch this instead of the removed file, so
`python run.py` still starts backend + a UI together.

**Still open:** the `DatasetSummary` contract is still this session's best-guess shape — reconcile
it with AI Developer 2 once their pipeline exists, since they'll be building on top of what's here.
