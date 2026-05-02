"""Shared fixtures.

The `valid_telemetry_payload` fixture returns a dict with all 20 schema fields
populated with valid values. Default uses `bssid_mode="hashed"` per D-03 (raw mode
is opt-in, default OFF) so the privacy-friendly path is what tests exercise by default.
"""
from __future__ import annotations

import pytest


@pytest.fixture
def valid_telemetry_payload() -> dict:
    """A telemetry frame dict that should validate cleanly against TelemetryFrame.

    All 20 fields populated. SHA-256-shaped bssid + bssid_mode='hashed' so the
    default-off raw-MAC opt-in (D-03) is what tests exercise by default.
    """
    return {
        # D-02 core 14
        "timestamp": 1_730_000_000.0,
        "os": "windows",
        "network_mode": "enterprise",
        "rssi_dbm": -62,
        "bssid": "a" * 64,                # 64-char SHA-256 hex
        "channel": 36,
        "ping_continuity": {
            "window_ms": 1000,
            "avg_rtt_ms": 18.5,
            "packet_loss_pct": 0.0,
            "jitter_ms": 1.2,
        },
        "latency_jitter_ms": 1.2,
        "dns_resolution_ms": 14.0,
        "dhcp_event_class": "none",
        "auth_event_class": "none",
        "captive_portal_detected": False,
        "mac_randomization_state": "off",
        "driver_state": "normal",
        # D-01 extended 4
        "per_packet_retry_count": 2,
        "rts_cts_rate": 0.05,
        "beacon_rssi_dbm": -64,
        "neighbor_ap_count_5ghz": 5,
        # D-03 / RESEARCH Open Question 2
        "bssid_mode": "hashed",
        # D-04
        "window_ms": 30000,
    }
