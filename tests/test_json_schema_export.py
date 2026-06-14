"""TelemetryFrame.model_json_schema() round-trips and surfaces additionalProperties: false.

Anthropic Structured Outputs consume the resulting JSON Schema directly.
"""

from __future__ import annotations

import json

from wifi_diag_schema.telemetry import TelemetryFrame


def test_telemetry_schema_roundtrips_through_json():
    schema = TelemetryFrame.model_json_schema()
    reparsed = json.loads(json.dumps(schema))
    assert reparsed == schema
    assert reparsed["title"] == "TelemetryFrame"
    assert reparsed["type"] == "object"


def test_telemetry_schema_is_closed():
    """`extra_forbidden` semantics surface as additionalProperties: false."""
    schema = TelemetryFrame.model_json_schema()
    assert schema.get("additionalProperties") is False, (
        "TelemetryFrame must export additionalProperties: false so Anthropic "
        "Structured Outputs reject unknown keys at the schema level."
    )


def test_required_core_fields_present():
    schema = TelemetryFrame.model_json_schema()
    required = set(schema.get("required", []))
    must_be_required = {
        "timestamp",
        "os",
        "network_mode",
        "rssi_dbm",
        "bssid",
        "bssid_mode",
        "channel",
        "ping_continuity",
        "dhcp_event_class",
        "auth_event_class",
        "captive_portal_detected",
        "mac_randomization_state",
        "driver_state",
        "window_ms",
    }
    missing = must_be_required - required
    assert not missing, f"Required fields missing from schema.required: {sorted(missing)}"


def test_verdict_top_class_enum_has_11_members_at_v1_2_0():
    """SCHEMA-01 sentinel: prevents accidental removal of 'unknown' or undocumented additions."""
    from wifi_diag_schema.verdict import Verdict

    schema = Verdict.model_json_schema()
    # top_class shows up via $defs reference or inline allOf depending on
    # Pydantic version; locate it. Pydantic v2 inlines Literal as an enum
    # directly under properties.top_class.enum
    enum_values = schema["properties"]["top_class"]["enum"]
    assert len(enum_values) == 11, (
        f"DisconnectClass count must be 11 at v1.2.0; got {len(enum_values)}: {enum_values}"
    )
    assert "unknown" in enum_values, f"'unknown' missing from DisconnectClass enum: {enum_values}"


def test_verdict_counter_evidence_in_schema_as_array_with_default():
    """SCHEMA-02 sentinel: counter_evidence MUST be in the JSON Schema as an optional array."""
    from wifi_diag_schema.verdict import Verdict

    schema = Verdict.model_json_schema()
    assert "counter_evidence" in schema["properties"], (
        f"counter_evidence missing from Verdict schema.properties: "
        f"{list(schema['properties'].keys())}"
    )
    ce = schema["properties"]["counter_evidence"]
    assert ce.get("type") == "array" or "items" in ce, f"counter_evidence shape unexpected: {ce}"
    # MUST NOT be in required
    required = set(schema.get("required", []))
    assert "counter_evidence" not in required, (
        f"counter_evidence must be optional (default_factory=list); "
        f"found in required: {sorted(required)}"
    )
