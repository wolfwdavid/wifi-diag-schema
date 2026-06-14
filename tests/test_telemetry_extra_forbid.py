"""FOUND-01: extra=forbid property test.

The schema source IS the privacy contract. Any unknown key on TelemetryFrame
must surface as a `extra_forbidden` ValidationError — adding a field requires
explicit allowlist + justification. Hypothesis exercises arbitrary unknown keys.
"""

from __future__ import annotations

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from wifi_diag_schema.telemetry import TelemetryFrame

ALLOWED_FIELDS: frozenset[str] = frozenset(
    {
        "timestamp",
        "os",
        "network_mode",
        "rssi_dbm",
        "bssid",
        "bssid_mode",
        "channel",
        "ping_continuity",
        "latency_jitter_ms",
        "dns_resolution_ms",
        "dhcp_event_class",
        "auth_event_class",
        "captive_portal_detected",
        "mac_randomization_state",
        "driver_state",
        "per_packet_retry_count",
        "rts_cts_rate",
        "beacon_rssi_dbm",
        "neighbor_ap_count_5ghz",
        "window_ms",
    }
)


@given(
    extra_key=st.text(min_size=1, max_size=64).filter(lambda k: k not in ALLOWED_FIELDS),
    extra_value=st.one_of(
        st.text(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
    ),
)
@settings(
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_unknown_key_is_rejected(valid_telemetry_payload, extra_key, extra_value):
    """Any field name not in the allowlist must raise extra_forbidden."""
    payload = {**valid_telemetry_payload, extra_key: extra_value}
    with pytest.raises(ValidationError) as exc_info:
        TelemetryFrame.model_validate(payload)
    # Pydantic v2 surfaces the canonical error type as 'extra_forbidden'.
    assert any(err["type"] == "extra_forbidden" for err in exc_info.value.errors()), (
        f"Expected extra_forbidden for key={extra_key!r}; "
        f"got {[err['type'] for err in exc_info.value.errors()]}"
    )


def test_obvious_forbidden_field_raw_message(valid_telemetry_payload):
    """Sanity: 'raw_message' is the canonical NEVER-add field per the schema docstring."""
    payload = {**valid_telemetry_payload, "raw_message": "anything"}
    with pytest.raises(ValidationError) as exc_info:
        TelemetryFrame.model_validate(payload)
    types = [err["type"] for err in exc_info.value.errors()]
    assert "extra_forbidden" in types
