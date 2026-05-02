"""D-03 + RESEARCH Open Question 2: bssid accepts BOTH raw MAC and 64-char SHA-256 hex.

The `bssid_mode` sibling field disambiguates which format is in use.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from wifi_diag_schema.telemetry import TelemetryFrame


def test_raw_mac_with_raw_mode_validates(valid_telemetry_payload):
    payload = {
        **valid_telemetry_payload,
        "bssid": "aa:bb:cc:dd:ee:ff",
        "bssid_mode": "raw",
    }
    frame = TelemetryFrame.model_validate(payload)
    assert frame.bssid == "aa:bb:cc:dd:ee:ff"
    assert frame.bssid_mode == "raw"


def test_sha256_hex_with_hashed_mode_validates(valid_telemetry_payload):
    payload = {
        **valid_telemetry_payload,
        "bssid": "f" * 64,
        "bssid_mode": "hashed",
    }
    frame = TelemetryFrame.model_validate(payload)
    assert frame.bssid == "f" * 64
    assert frame.bssid_mode == "hashed"


def test_arbitrary_string_rejected(valid_telemetry_payload):
    payload = {
        **valid_telemetry_payload,
        "bssid": "not-a-mac-or-hash",
    }
    with pytest.raises(ValidationError):
        TelemetryFrame.model_validate(payload)


def test_uppercase_mac_rejected(valid_telemetry_payload):
    """Pattern requires lowercase hex — agents must normalize to lowercase."""
    payload = {
        **valid_telemetry_payload,
        "bssid": "AA:BB:CC:DD:EE:FF",
        "bssid_mode": "raw",
    }
    with pytest.raises(ValidationError):
        TelemetryFrame.model_validate(payload)


def test_invalid_bssid_mode_rejected(valid_telemetry_payload):
    payload = {
        **valid_telemetry_payload,
        "bssid_mode": "plaintext",  # not in BssidMode literal
    }
    with pytest.raises(ValidationError):
        TelemetryFrame.model_validate(payload)
