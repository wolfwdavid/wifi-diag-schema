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
        "timestamp", "os", "network_mode", "rssi_dbm", "bssid", "bssid_mode",
        "channel", "ping_continuity",
        "dhcp_event_class", "auth_event_class",
        "captive_portal_detected", "mac_randomization_state", "driver_state",
        "window_ms",
    }
    missing = must_be_required - required
    assert not missing, f"Required fields missing from schema.required: {sorted(missing)}"
