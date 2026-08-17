"""Validates every prompt template in the library renders cleanly and that guardrails are present."""

import pytest

from backend.app.prompts.loader import apply_medical_guardrails, load_medical_disclaimer, load_prompt

TEMPLATES_WITH_DUMMY_VARS = {
    "system/research_copilot_v1.yaml": {
        "context_text": "dummy context",
        "citation_lines": "[1] dummy source",
        "route": "rag",
    },
    "system/student_tutor_v1.yaml": {"topic": "estrogen", "level": "beginner"},
    "system/hormone_education_v1.yaml": {"question": "What is PCOS?"},
    "system/report_generator_v1.yaml": {"topic": "PCOS", "source_summaries": "[1] dummy summary"},
    "tasks/summarize_paper_v1.yaml": {"paper_text": "dummy paper text"},
    "tasks/extract_entities_v1.yaml": {"text": "dummy text"},
    "tasks/generate_quiz_v1.yaml": {"topic": "PCOS", "num_questions": 5, "difficulty": "medium"},
    "tasks/interpret_dataset_v1.yaml": {"dataset_summary": "{}"},
}


@pytest.mark.parametrize("relative_path,dummy_vars", TEMPLATES_WITH_DUMMY_VARS.items())
def test_template_renders_without_leftover_placeholders(relative_path, dummy_vars):
    template = load_prompt(relative_path)
    rendered = template.render(**dummy_vars)

    assert rendered.strip()
    assert "{{" not in rendered
    assert "}}" not in rendered


def test_medical_disclaimer_loads_and_mentions_professional_advice():
    disclaimer = load_medical_disclaimer()
    assert "not a substitute for professional medical advice" in disclaimer


def test_apply_medical_guardrails_appends_disclaimer():
    base_prompt = "You are a helpful assistant."
    guarded = apply_medical_guardrails(base_prompt)

    assert base_prompt in guarded
    assert "not a substitute for professional medical advice" in guarded
