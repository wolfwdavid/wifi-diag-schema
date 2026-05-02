"""Verdict.model_json_schema() is Anthropic-Structured-Outputs-shaped.

Structural smoke only — does not actually call Anthropic. Plan 01-02's handshake
test will exercise schema_version + Verdict.schema_version round-trip.
"""
from __future__ import annotations

from wifi_diag_schema.verdict import Verdict


def test_verdict_schema_is_closed_object():
    schema = Verdict.model_json_schema()
    assert schema["type"] == "object"
    assert schema.get("additionalProperties") is False


def test_verdict_schema_has_required_properties():
    schema = Verdict.model_json_schema()
    properties = schema["properties"]
    required_keys = (
        "top_class", "confidence", "top_k",
        "headline", "suggested_fix", "evidence",
    )
    for required_key in required_keys:
        assert required_key in properties, (
            f"Verdict schema missing property: {required_key}"
        )


def test_verdict_top_class_is_enum():
    """top_class must surface as a closed enum (the 10 canonical class slugs)
    so Anthropic constrains generation to valid labels.
    """
    schema = Verdict.model_json_schema()
    properties = schema["properties"]
    top_class = properties["top_class"]
    # Pydantic Literal -> JSON Schema 'enum'
    assert "enum" in top_class, (
        "Verdict.top_class must export as JSON Schema 'enum' so Anthropic "
        "Structured Outputs constrain output to valid class slugs."
    )
    assert len(top_class["enum"]) == 10
