"""Unit tests for deterministic citation formatting. Pure logic, no API keys required."""

from backend.app.services.citation_service import format_apa, format_bibtex, format_vancouver

FULL_PAPER = {
    "title": "Insulin Resistance and PCOS: A Review",
    "authors": ["Jane A Doe", "John B Smith"],
    "year": 2021,
    "journal": "Journal of Endocrinology",
    "doi": "10.1000/xyz123",
    "url": "https://example.com/paper",
}


def test_apa_full_paper():
    citation = format_apa(FULL_PAPER)
    assert "Doe, J. A., & Smith, J. B." in citation
    assert "(2021)" in citation
    assert "Insulin Resistance and PCOS: A Review" in citation
    assert "https://doi.org/10.1000/xyz123" in citation


def test_apa_missing_authors_and_year():
    paper = {"title": "Untitled Study", "authors": [], "year": None, "doi": None, "url": None}
    citation = format_apa(paper)
    assert "(n.d.)" in citation
    assert "Untitled Study" in citation


def test_apa_missing_doi_falls_back_to_url():
    paper = {**FULL_PAPER, "doi": None}
    citation = format_apa(paper)
    assert "https://example.com/paper" in citation
    assert "doi.org" not in citation


def test_vancouver_more_than_six_authors_uses_et_al():
    authors = [f"First{i} Last{i}" for i in range(8)]
    paper = {**FULL_PAPER, "authors": authors}
    citation = format_vancouver(paper)
    assert citation.count(",") >= 5
    assert citation.split(".")[0].strip().endswith("et al")


def test_vancouver_six_or_fewer_authors_lists_all():
    authors = [f"First{i} Last{i}" for i in range(3)]
    paper = {**FULL_PAPER, "authors": authors}
    citation = format_vancouver(paper)
    assert "et al" not in citation
    for i in range(3):
        assert f"Last{i}" in citation


def test_vancouver_missing_authors_does_not_crash():
    paper = {**FULL_PAPER, "authors": []}
    citation = format_vancouver(paper)
    assert "Insulin Resistance" in citation


def test_bibtex_contains_required_fields():
    bibtex = format_bibtex(FULL_PAPER)
    assert bibtex.startswith("@article{")
    assert "title = {Insulin Resistance and PCOS: A Review}" in bibtex
    assert "author = {Jane A Doe and John B Smith}" in bibtex
    assert "doi = {10.1000/xyz123}" in bibtex
    assert bibtex.strip().endswith("}")


def test_bibtex_missing_optional_fields_omits_them():
    paper = {"title": "Solo Study", "authors": [], "year": None, "doi": None, "url": None, "journal": None}
    bibtex = format_bibtex(paper)
    assert "author = " not in bibtex
    assert "journal = " not in bibtex
    assert "title = {Solo Study}" in bibtex


def test_bibtex_key_has_no_special_characters():
    paper = {**FULL_PAPER, "title": "Insulin: Resistance & PCOS!"}
    bibtex = format_bibtex(paper)
    key_line = bibtex.splitlines()[0]
    key = key_line[len("@article{"):-1]
    assert key.isalnum()
