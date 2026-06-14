"""FOUND-01 literal allowlist regression gate (Pitfall 1 mitigation).

Every TelemetryFrame field is enumerated below. Adding or removing a field from
the schema source without updating this set fails CI — this is the explicit
"adding a field is a deliberate, reviewable act" enforcement.

When you add a field intentionally, update BOTH this set AND the
`why-allowlisted` justification in `_justifications.py` (Pitfall 1 contract).
"""

from __future__ import annotations

from wifi_diag_schema.telemetry import TelemetryFrame

EXPECTED_FIELDS: frozenset[str] = frozenset(
    {
        # D-02 core 14
        "timestamp",
        "os",
        "network_mode",
        "rssi_dbm",
        "bssid",
        "channel",
        "ping_continuity",
        "latency_jitter_ms",
        "dns_resolution_ms",
        "dhcp_event_class",
        "auth_event_class",
        "captive_portal_detected",
        "mac_randomization_state",
        "driver_state",
        # D-01 extended 4
        "per_packet_retry_count",
        "rts_cts_rate",
        "beacon_rssi_dbm",
        "neighbor_ap_count_5ghz",
        # D-03 / RESEARCH Open Question 2
        "bssid_mode",
        # D-04
        "window_ms",
    }
)


def test_field_count_is_twenty():
    assert len(TelemetryFrame.model_fields) == 20, (
        f"Expected exactly 20 fields (14 core + 4 extended + bssid_mode + window_ms); "
        f"got {len(TelemetryFrame.model_fields)}"
    )


def test_field_names_match_allowlist():
    actual = set(TelemetryFrame.model_fields.keys())
    extra = actual - EXPECTED_FIELDS
    missing = EXPECTED_FIELDS - actual
    assert not extra, (
        f"TelemetryFrame has fields not in the allowlist: {sorted(extra)}. "
        f"Update tests/test_telemetry_field_allowlist.py AND _justifications.py "
        f"(Pitfall 1 — privacy contract)."
    )
    assert not missing, (
        f"TelemetryFrame is missing fields the allowlist requires: {sorted(missing)}"
    )
