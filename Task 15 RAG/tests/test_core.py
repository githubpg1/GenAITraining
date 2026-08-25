from pathlib import Path
import pytest
from src.ingestion.parser import detect_sections
from src.ingestion.chunker import chunk_sections
from src.generation.grounding_validator import validate_answer
from src.generation.generator import mock_answer


def test_sections_detected():
    sections = detect_sections("1 Purpose\nApplies to employees.\n3.1 Entitlement\nEmployees receive 20 days.")
    assert len(sections) == 2
    assert sections[1][0] == "3.1"


def test_chunk_metadata_and_deterministic_id():
    chunks = chunk_sections([("3.1", "Entitlement", "Employees receive 20 vacation days.")], "time-off-2026", "Employee Time Off Policy", "3.0", "2026-01-01", "policy.pdf")
    assert chunks[0].chunk_id == chunk_sections([("3.1", "Entitlement", "Employees receive 20 vacation days.")], "time-off-2026", "Employee Time Off Policy", "3.0", "2026-01-01", "policy.pdf")[0].chunk_id
    assert chunks[0].metadata["section_number"] == "3.1"
    assert chunks[0].metadata["version"] == "3.0"


def test_grounding_rejects_unsupported_number():
    result = [{"text": "Employees receive 20 vacation days.", "metadata": {"document_name": "Policy", "section": "3.1"}}]
    assert not validate_answer("Employees receive 99 vacation days.", [{"document": "Policy", "section": "3.1"}], result)


def test_grounded_mock_answer_cites_source():
    result = [{"text": "3.1 Entitlement\nEmployees receive 20 vacation days.", "metadata": {"document_name": "Policy", "section": "3.1 Entitlement", "page_number": 1, "version": "3.0", "effective_date": "2026-01-01"}}]
    answer = mock_answer("How many vacation days do employees receive?", result)
    assert answer["citations"][0]["section"] == "3.1 Entitlement"
    assert "20" in answer["answer"]


def test_ambiguous_leave():
    answer = mock_answer("How much leave do I get?", [{"text": "leave", "metadata": {"document_name": "Policy", "section": "1"}}])
    assert answer["classification"] == "AMBIGUOUS"
