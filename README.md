# 🧬 HormoneBench AI

An AI-powered ecosystem for women's hormonal health research, education, and awareness.

This repository is a **monorepo** with two main parts that run separately and talk to each other over HTTP:

```
Hormone-Bench-AI/
├── backend/        Python FastAPI service — the AI/RAG engine (chat, literature search, reports, etc.)
├── frontend/        Next.js web app — the user-facing website (login, dashboard, chat UI)
└── Documentation/    Project planning PDFs (hackathon plan, ecosystem overview, team structure)
```

**New to this project? New to coding in general?** This README is written so that a complete
beginner can get both halves of the app running on their own computer. Follow it top to bottom —
don't skip steps.

---

## Table of Contents

1. [What this project actually does](#what-this-project-actually-does)
2. [Before you start — install these tools](#before-you-start--install-these-tools)
3. [Getting the code](#getting-the-code)
4. [Setting up the backend (Python/FastAPI)](#setting-up-the-backend-pythonfastapi)
5. [Setting up the frontend (Next.js)](#setting-up-the-frontend-nextjs)
6. [Running everything together](#running-everything-together)
7. [Project structure explained](#project-structure-explained)
8. [Testing](#testing)
9. [Common problems & fixes](#common-problems--fixes)
10. [License](#license)

---

## What this project actually does

HormoneBench AI has two halves:

- **`backend/`** is the "brain." It's a Python API server that uses AI (Groq's LLM + Google
  Gemini embeddings) to power features like:
  - A research chatbot ("Research Copilot") that can search the web, read documents, and answer questions
  - Searching medical literature (PubMed, Semantic Scholar)
  - Summarizing research papers
  - Generating citations (APA, Vancouver, BibTeX)
  - Analyzing uploaded datasets/CSV files with real statistics
  - A student tutor (quizzes, flashcards, explanations)
  - A public hormone-health Q&A agent (with a built-in medical disclaimer)
  - A biomedical knowledge graph

- **`frontend/`** is the "face." It's a Next.js website (the thing users actually see and click
  around in) with login/signup (via Firebase Authentication) and a dashboard that talks to the
  backend.

You need **both** running at the same time to use the full app. The backend can also be tested
completely on its own (via its interactive API docs) without the frontend running at all.

---

## Before you start — install these tools

You only need to do this section once per computer.

| Tool | Why you need it | Check if installed | Install from |
|---|---|---|---|
| **Python 3.11+** | Runs the backend | `python3 --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **Node.js 20+** (includes `npm`) | Runs the frontend | `node --version` | [nodejs.org](https://nodejs.org/) |
| **Git** | Downloads/manages the code | `git --version` | [git-scm.com](https://git-scm.com/downloads) |
| **A code editor** | Editing files | — | [VS Code](https://code.visualstudio.com/) recommended |

Open a terminal (Mac: **Terminal** app, Windows: **PowerShell** or **Git Bash**) and run the
"Check if installed" commands above. If any command says "command not found," install that tool
before continuing.

You will also need **free API keys** from a couple of external services before the backend will
fully work (details in the backend setup section below).

---

## Getting the code

If you haven't already cloned this repository:

```bash
git clone <this-repository-url>
cd Hormone-Bench-AI
```

If you already have it (e.g. you're reading this file from a local copy), just open a terminal
in the project's root folder (`Hormone-Bench-AI/`).

---

## Setting up the backend (Python/FastAPI)

All commands in this section are run from the `backend/` folder.

```bash
cd backend
```

### 1. Create a virtual environment

A virtual environment keeps this project's Python packages separate from everything else on your
computer.

```bash
python3 -m venv .venv
```

Activate it (you need to do this every time you open a new terminal to work on the backend):

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

You'll know it worked because your terminal prompt will now start with `(.venv)`.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This downloads all the Python libraries the backend needs (FastAPI, LangGraph, ChromaDB, etc.).
It can take a few minutes the first time.

### 3. Configure environment variables (API keys)

Copy the example environment file:

```bash
cp .env.example .env
```

Open the new `.env` file in your editor and fill in the values:

```env
# Required — the backend will not start without these two
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Optional — raises PubMed / Semantic Scholar rate limits, not required to function
NCBI_API_KEY=
SEMANTIC_SCHOLAR_API_KEY=

# Optional — enables extra tools (web search, reading URLs)
TAVILY_API_KEY=
FIRECRAWL_API_KEY=
```

Where to get the required keys (both have free tiers):

- **`GROQ_API_KEY`** — sign up at [console.groq.com](https://console.groq.com/), create an API key.
- **`GOOGLE_API_KEY`** — go to [Google AI Studio](https://aistudio.google.com/apikey), create an
  API key (used for Gemini embeddings).

Everything else in `.env` is optional — the app will still run without them, just with reduced
functionality (e.g. lower rate limits, or a tool returning empty results instead of live data).

**Never commit your `.env` file to git.** It's already excluded via `.gitignore`.

### 4. Start the backend server

Make sure your virtual environment is still active (prompt starts with `(.venv)`), then:

```bash
uvicorn app.main:app --reload
```

If it worked, you'll see something like `Uvicorn running on http://0.0.0.0:8000`. Leave this
terminal window open — the server keeps running here.

Open your browser to **http://localhost:8000/docs** — this is an interactive page (Swagger UI)
where you can try every backend feature by clicking buttons, without writing any code. This is
the easiest way to confirm the backend works.

---

## Setting up the frontend (Next.js)

Open a **new terminal window** (leave the backend running in the other one), then from the
project root:

```bash
cd frontend
```

### 1. Install dependencies

```bash
npm install
```

This downloads all the JavaScript/TypeScript packages the frontend needs (Next.js, React,
Firebase, etc.). It can take a few minutes the first time.

### 2. Configure environment variables

The frontend uses [Firebase](https://firebase.google.com/) for user login/signup. Create a file
named `.env.local` inside `frontend/`:

```env
# Firebase client config (from Firebase Console → Project Settings → General → Your apps)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin SDK config (from Firebase Console → Project Settings → Service Accounts → Generate new private key)
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=
```

To get these values:

1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project
   (or use an existing one).
2. **Client config**: Project Settings → General → "Your apps" → add a Web app → copy the config
   values shown there.
3. **Admin config**: Project Settings → Service Accounts → "Generate new private key" → this
   downloads a JSON file containing `project_id`, `client_email`, and `private_key`.
   - Paste `private_key` exactly as-is, including the quotes and `\n` characters.
4. Also enable **Authentication → Sign-in method → Email/Password** (or whichever providers you
   want) in the Firebase Console, or login/signup won't work.

### 3. Start the frontend dev server

```bash
npm run dev
```

Open your browser to **http://localhost:3000**. You should see the HormoneBench AI website.

---

## Running everything together

Once both are set up, day-to-day you just need two terminals open:

**Terminal 1 — backend:**
```bash
cd backend
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 — frontend:**
```bash
cd frontend
npm run dev
```

Then visit **http://localhost:3000** for the website, and **http://localhost:8000/docs** for the
raw backend API.

There's also a legacy Streamlit test dashboard for manually exercising every backend endpoint
without the Next.js frontend:

```bash
cd backend
streamlit run frontend/test_dashboard.py
```
Runs at **http://localhost:8501**.

---

## Project structure explained

```text
Hormone-Bench-AI/
├── Documentation/              Planning PDFs (hackathon plan, ecosystem overview, team structure)
│
├── backend/                    Python FastAPI AI service
│   ├── app/
│   │   ├── main.py             FastAPI entrypoint
│   │   ├── config.py           Environment/settings loader
│   │   ├── api/                One router per feature (literature, papers, tutor, etc.)
│   │   ├── agents/              LangGraph state graph — the Research Copilot's "brain"
│   │   ├── rag/                 Document loading, chunking, embeddings, ChromaDB vector store
│   │   ├── services/            Business logic behind each API route
│   │   ├── prompts/              Versioned prompt templates + medical safety guardrails
│   │   ├── schemas/              Shared data models (Pydantic)
│   │   ├── memory/               SQLite-backed conversation history
│   │   ├── tools/                Web search / URL reading helper tools
│   │   └── utils/                Logging, caching, exceptions
│   ├── frontend/test_dashboard.py   Streamlit dashboard for manually testing every backend endpoint
│   ├── scripts/                 Standalone scripts (smoke tests, knowledge-graph extraction)
│   ├── tests/                   Automated pytest unit tests
│   ├── data/                    Local database/vector-store files (auto-created, gitignored)
│   ├── requirements.txt         Python dependencies
│   ├── run.py                   Launches backend + test dashboard together
│   └── .env.example             Template for backend environment variables
│
└── frontend/                    Next.js website (what users see)
    ├── app/                     Pages and routes (Next.js App Router)
    │   ├── (app)/                Logged-in app pages (dashboard, etc.)
    │   ├── (auth)/                Login/signup pages
    │   └── api/                  Frontend's own API routes (e.g. session handling)
    ├── components/               Reusable UI pieces (dashboard, layout, marketing, ui primitives)
    ├── contexts/                  React context providers (e.g. auth state)
    ├── lib/
    │   ├── firebase/              Firebase client & admin SDK setup
    │   ├── auth/                  Auth session helpers, error messages
    │   └── nav.ts, utils.ts       Navigation config, small helpers
    ├── hooks/                     Custom React hooks
    ├── public/                    Static assets (images, icons)
    └── package.json               Node.js dependencies and scripts
```

---

## Testing

### Backend

```bash
cd backend
source .venv/bin/activate

# Unit tests — pure logic, no server or API keys required
pytest tests/

# Live end-to-end test against every endpoint — requires the backend running with real API keys
python scripts/smoke_test.py

# Skip LLM-dependent endpoints for a quick structural check
SKIP_LLM_TESTS=1 python scripts/smoke_test.py
```

Quick manual check: open **http://localhost:8000/docs**, try `GET /api/v1/literature/search?q=PCOS`
to confirm live PubMed/Semantic Scholar connectivity.

### Frontend

```bash
cd frontend
npm run lint
```

---

## Common problems & fixes

| Problem | Likely cause | Fix |
|---|---|---|
| `command not found: python3` / `uvicorn` | Python not installed, or venv not activated | Install Python; re-run `source .venv/bin/activate` |
| Backend crashes on startup mentioning `GOOGLE_API_KEY` or `GROQ_API_KEY` | Missing/empty `.env` values | Fill in both required keys in `backend/.env` |
| `npm install` fails or is very slow | Node.js version too old | Install Node.js 20+ from [nodejs.org](https://nodejs.org/) |
| Frontend shows a Firebase config error | Missing/incorrect `.env.local` values | Double-check every `NEXT_PUBLIC_FIREBASE_*` and `FIREBASE_*` value against your Firebase project |
| Frontend can't reach the backend | Backend not running, or wrong URL | Make sure `uvicorn` is running on port 8000 in a separate terminal |
| Port `8000` or `3000` already in use | Another process is using that port | Stop the other process, or run on a different port (`uvicorn app.main:app --reload --port 8001`) |
| Changes to `.env` / `.env.local` don't take effect | Server was already running | Stop the server (Ctrl+C) and start it again |

---

## License

Distributed under the MIT License. See [`backend/LICENSE`](backend/LICENSE) for details.
