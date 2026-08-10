"""Loader for the versioned prompt library (app/prompts/library/**/*.yaml)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import yaml
from jinja2 import Template

from app.config import settings

LIBRARY_DIR = Path(settings.PROMPT_LIBRARY_DIR)
GUARDRAILS_DIR = LIBRARY_DIR / "guardrails"


class PromptTemplate:
    """A rendered-on-demand prompt template loaded from the library."""

    def __init__(self, prompt_id: str, version: str, system_prompt: str, input_variables: List[str]):
        self.id = prompt_id
        self.version = version
        self.input_variables = input_variables
        self._template = Template(system_prompt)

    def render(self, **kwargs: Any) -> str:
        return self._template.render(**kwargs).strip()


@lru_cache(maxsize=None)
def _load_yaml(relative_path: str) -> Dict[str, Any]:
    path = LIBRARY_DIR / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=None)
def load_prompt(relative_path: str) -> PromptTemplate:
    """Load and cache a prompt template, e.g. load_prompt('system/research_copilot_v1.yaml')."""
    data = _load_yaml(relative_path)
    return PromptTemplate(
        prompt_id=data["id"],
        version=data["version"],
        system_prompt=data["system_prompt"],
        input_variables=data.get("input_variables", []),
    )


@lru_cache(maxsize=1)
def load_medical_disclaimer() -> str:
    raw = (GUARDRAILS_DIR / "medical_disclaimer.txt").read_text(encoding="utf-8").strip()
    return " ".join(raw.split())


def apply_medical_guardrails(system_prompt: str) -> str:
    """Append the canonical medical disclaimer to any patient/public-facing system prompt."""
    return f"{system_prompt}\n\n---\n{load_medical_disclaimer()}"
