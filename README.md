# 🧬 HormoneBench AI — Research AI Backend

> AI Developer 1's ("Research AI Engineer") backend service for **HormoneBench AI**, an
> AI-powered ecosystem for women's hormonal health research, education, and awareness.

Built on **LangGraph**, **Groq** (LLM generation), **Google Gemini** (embeddings), **ChromaDB**
(vector store), and **FastAPI**. Originated from a generic RAG chatbot starter ("RAGentic AI")
and extended into the full AI Developer 1 scope: a Research Copilot, literature search, paper
summarization, citation generation, research reports, dataset/statistical analysis, a biomedical
knowledge graph, a student tutor, and a public hormone-education agent.

---

## ✨ Features

| Area | What it does |
|---|---|
| **Research Copilot** | Session-based chat that routes between RAG, live web search, URL reading, or general LLM reasoning (LangGraph state graph), with persistent SQLite-backed thread memory |
| **Literature Search** | Live search across PubMed (NCBI E-utilities) and Semantic Scholar, deduped and normalized, with result caching |
| **Paper Summarization** | Structured summaries (background, methods, findings, limitations, plain-language) from a DOI, PMID, raw text, or an uploaded PDF/DOCX/TXT |
| **RAG** | Upload documents or ingest literature search results directly into a persistent ChromaDB corpus for grounded, cited answers |
| **Semantic Search** | Query the ingested RAG corpus directly, no generation |
| **Citation Generator** | Deterministic (non-LLM) APA, Vancouver, and BibTeX formatting |
| **Research Report Generator** | Auto-gathers sources and produces a structured Markdown report with a formatted reference list |
| **Dataset Analysis** | AI narrative interpretation over a structured dataset summary |
| **Statistical Analysis Assistant** | Upload a raw CSV and get real computed statistics (descriptive stats, correlations, outliers, hormonal-biomarker detection) — optionally with an AI narrative layered on top |
| **Evidence Summarizer** | Pulls literature + RAG corpus evidence for a claim/topic into a concise, caveated summary |
| **Student AI Tutor** | Concept explanations, quizzes, flashcards, and study notes |
| **Hormone Education Agent** | Public Q&A with a mandatory medical disclaimer guardrail |
| **Biomedical Knowledge Graph** | Lightweight SQLite + NetworkX entity/relationship extraction and Q&A |
| **Prompt Library** | Versioned, Jinja2-templated prompts (`app/prompts/library/`) shared across every service |

---

## 🏗️ Tech Stack

- **Orchestration:** LangGraph / LangChain
- **LLM Engine:** Groq (`llama-3.3-70b-versatile`)
- **Embedding Model:** Google Gemini (`gemini-embedding-001`, with automatic model fallback)
- **Vector Store:** ChromaDB (local persistent storage)
- **Knowledge Graph:** SQLite + NetworkX
- **Backend API:** FastAPI / Uvicorn
- **Testing Dashboard:** Streamlit (`frontend/test_dashboard.py`)
- **External APIs:** NCBI E-utilities (PubMed), Semantic Scholar Graph API, Tavily (web search), Firecrawl (URL reading)

---

## 🛠️ Project Structure

```text
app/
├── main.py                    # FastAPI entrypoint
├── config.py                  # Environment/settings (pydantic-settings)
├── api/                       # One router module per feature, all mounted under /api/v1
│   ├── routes.py              #   aggregates every router below + /health, /chat, /documents/upload
│   ├── literature.py          #   /literature/search, /literature/ingest
│   ├── papers.py              #   /papers/summarize(/upload)
│   ├── search.py               #   /search/semantic
│   ├── citations.py           #   /citations/format
│   ├── reports.py             #   /reports/generate
│   ├── dataset_analysis.py    #   /dataset-analysis/interpret
│   ├── statistics.py          #   /statistics/analyze(/full)
│   ├── evidence.py            #   /evidence/summarize
│   ├── tutor.py               #   /tutor/explain|quiz|flashcards|notes
│   ├── education.py           #   /education/ask
│   └── knowledge_graph.py     #   /kg/extract, /kg/entity/{name}, /kg/ask
├── agents/                    # LangGraph state, nodes, router (the Research Copilot engine)
├── rag/                       # Document loading, chunking, embeddings, Chroma vectorstore, retriever
├── services/                  # Business logic behind every router (one file per feature)
├── prompts/                   # Versioned prompt library + Jinja2 loader + medical guardrails
├── schemas/                   # Shared pydantic models (Paper, Citation, DatasetSummary, Quiz, ...)
├── memory/                    # SQLite-backed LangGraph conversation checkpointer
├── tools/                     # Web search, URL reader (bonus tools beyond core AI Dev 1 scope)
└── utils/                     # Logging, exceptions, TTL cache, citation helpers

frontend/
└── test_dashboard.py          # 13-tab Streamlit dashboard for manually testing every endpoint

scripts/
├── smoke_test.py              # httpx script hitting every endpoint on a running server
└── extract_kg.py              # offline batch knowledge-graph extraction over uploaded documents

tests/                         # pytest unit tests (citation formatting, prompt rendering, statistics)
data/                          # ChromaDB + SQLite storage (gitignored, created automatically)
run.py                         # Launches backend + test dashboard together
```

---

## ⚙️ Installation & Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
# Required — the app will not start without these
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Optional — raise PubMed / Semantic Scholar rate limits, not required to function
NCBI_API_KEY=
SEMANTIC_SCHOLAR_API_KEY=

# Optional — existing web_search / url_reader tools
TAVILY_API_KEY=
FIRECRAWL_API_KEY=
```

`GOOGLE_API_KEY` and `GROQ_API_KEY` are the only two required to boot the app. Everything else
degrades gracefully when absent (lower rate limits, or a tool simply returns empty results).

---

## 🚀 Running the Application

### Start the backend (FastAPI)

```bash
uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`. Interactive API docs (Swagger UI) at `http://localhost:8000/docs`.

### Start the test dashboard (Streamlit)

```bash
streamlit run frontend/test_dashboard.py
```
Runs at `http://localhost:8501`. One tab per feature — set the backend URL in the sidebar and
click "Check health" to confirm the connection.

### Or run both together

```bash
python run.py
```

---

## 🧪 Testing

```bash
# Unit tests — pure logic, no server or API keys required
pytest tests/

# Live end-to-end test against every endpoint — requires the backend running with real keys
python scripts/smoke_test.py

# Skip LLM-dependent endpoints for a quick structural check
SKIP_LLM_TESTS=1 python scripts/smoke_test.py
```

### Quick manual test workflow

1. Open the **Swagger UI** at `http://localhost:8000/docs` or the **test dashboard** at `http://localhost:8501`.
2. Try `POST /api/v1/tutor/quiz` with `{"topic": "PCOS", "num_questions": 3, "difficulty": "medium"}` — this exercises the prompt library, Groq structured-output generation, and pydantic schema validation in one call.
3. Try `GET /api/v1/literature/search?q=PCOS insulin resistance` to confirm live PubMed + Semantic Scholar connectivity.

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.
