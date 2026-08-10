"""Biomedical Knowledge Graph: lightweight SQLite + NetworkX Q&A over extracted entity
relationships. Deliberately not a full graph database (e.g. Neo4j) — that's disproportionate
infra for a hackathon-scale corpus (dozens to low hundreds of documents). Triples are extracted
offline via Gemini/Groq structured output and stored in SQLite; NetworkX handles in-memory
1-2 hop traversal for Q&A."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

import networkx as nx
from pydantic import BaseModel, Field

from app.config import settings
from app.llm.groq import get_llm
from app.prompts.loader import load_prompt
from app.utils.exceptions import AppBaseException
from app.utils.logger import logger


class KGTriple(BaseModel):
    subject: str
    relation: str
    object: str


class KGExtraction(BaseModel):
    triples: List[KGTriple] = Field(default_factory=list)


class KnowledgeGraphError(AppBaseException):
    """Raised when extraction or graph querying fails."""


def _get_connection() -> sqlite3.Connection:
    db_path = Path(settings.KG_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS triples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            relation TEXT NOT NULL,
            object TEXT NOT NULL,
            source TEXT
        )
        """
    )
    conn.commit()
    return conn


def extract_triples(text: str) -> List[KGTriple]:
    """Run a single structured-output LLM call to pull (subject, relation, object) triples
    out of a chunk of text."""
    prompt_template = load_prompt("tasks/extract_entities_v1.yaml")
    rendered = prompt_template.render(text=text[:8000])

    try:
        structured_llm = get_llm().with_structured_output(KGExtraction)
        result: KGExtraction = structured_llm.invoke(rendered)
        return result.triples
    except Exception as exc:
        logger.exception("Knowledge graph extraction failed: %s", exc)
        raise KnowledgeGraphError(f"Failed to extract entities: {exc}") from exc


def store_triples(triples: List[KGTriple], source: Optional[str] = None) -> int:
    if not triples:
        return 0

    conn = _get_connection()
    try:
        conn.executemany(
            "INSERT INTO triples (subject, relation, object, source) VALUES (?, ?, ?, ?)",
            [(t.subject.strip(), t.relation.strip(), t.object.strip(), source) for t in triples],
        )
        conn.commit()
        return len(triples)
    finally:
        conn.close()


def extract_and_store(text: str, source: Optional[str] = None) -> int:
    triples = extract_triples(text)
    return store_triples(triples, source)


def _load_all_triples() -> List[Dict[str, Any]]:
    conn = _get_connection()
    try:
        rows = conn.execute("SELECT subject, relation, object, source FROM triples").fetchall()
        return [{"subject": r[0], "relation": r[1], "object": r[2], "source": r[3]} for r in rows]
    finally:
        conn.close()


def build_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    for row in _load_all_triples():
        graph.add_edge(row["subject"], row["object"], relation=row["relation"], source=row["source"])
    return graph


def get_entity(name: str) -> Dict[str, Any]:
    graph = build_graph()
    matches = [n for n in graph.nodes if n.lower() == name.lower()]
    if not matches:
        matches = [n for n in graph.nodes if name.lower() in n.lower()]
    if not matches:
        return {"entity": name, "relations": []}

    node = matches[0]
    relations = []
    for _, target, data in graph.out_edges(node, data=True):
        relations.append(
            {"subject": node, "relation": data.get("relation"), "object": target, "source": data.get("source")}
        )
    for source, _, data in graph.in_edges(node, data=True):
        relations.append(
            {"subject": source, "relation": data.get("relation"), "object": node, "source": data.get("source")}
        )

    return {"entity": node, "relations": relations}


def _find_entities_in_question(question: str, graph: nx.DiGraph) -> List[str]:
    question_lower = question.lower()
    return [n for n in graph.nodes if n.lower() in question_lower]


async def ask(question: str) -> Dict[str, Any]:
    graph = build_graph()
    if graph.number_of_nodes() == 0:
        raise KnowledgeGraphError(
            "The knowledge graph is empty. Extract entities from documents first (POST /kg/extract "
            "or run scripts/extract_kg.py)."
        )

    matched_entities = _find_entities_in_question(question, graph)
    facts: List[str] = []

    for entity in matched_entities:
        for _, target, data in graph.out_edges(entity, data=True):
            facts.append(f"{entity} {data.get('relation')} {target}")
        for source, _, data in graph.in_edges(entity, data=True):
            facts.append(f"{source} {data.get('relation')} {entity}")

    if not facts:
        raise KnowledgeGraphError(
            f"No known entities from the question were found in the knowledge graph: '{question}'"
        )

    facts_text = "\n".join(f"- {f}" for f in facts[:30])
    prompt = (
        "You are answering a question using ONLY the following knowledge graph facts. "
        "If the facts are insufficient to fully answer, say so clearly.\n\n"
        f"Facts:\n{facts_text}\n\nQuestion: {question}"
    )

    try:
        llm = get_llm()
        response = llm.invoke(prompt)
    except Exception as exc:
        logger.exception("Knowledge graph Q&A failed: %s", exc)
        raise KnowledgeGraphError(f"Failed to answer from knowledge graph: {exc}") from exc

    return {"answer": response.content, "facts_used": facts[:30]}
