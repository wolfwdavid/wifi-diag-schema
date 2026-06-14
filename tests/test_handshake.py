"""FOUND-03 schema-version handshake (D-05).

Compatibility matrix:
- patch difference   -> "match" silently
- minor difference   -> "minor_drift" + UserWarning
- major difference   -> raise IncompatibleSchemaError with upgrade-link UX
"""

from __future__ import annotations

import warnings

import pytest
from pydantic import ValidationError

from wifi_diag_schema import (
    SCHEMA_VERSION,
    HandshakeFrame,
    IncompatibleSchemaError,
    TelemetryFrameLenient,
    check_compatibility,
    make_handshake,
)


def test_match_returns_match_silently():
    """Identical versions: silent match."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any warning fails this test
        assert check_compatibility("1.0.0", "1.0.0") == "match"


def test_patch_mismatch_returns_match_silently():
    """Patch is doc-only per D-05 — no warning, returns match."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert check_compatibility("1.0.0", "1.0.5") == "match"


def test_minor_mismatch_returns_minor_drift_with_warning():
    """Minor mismatch: returns minor_drift AND warns loudly (Pitfall 3 mitigation)."""
    with pytest.warns(UserWarning, match="minor"):
        result = check_compatibility("1.0.0", "1.1.0")
    assert result == "minor_drift"


def test_major_mismatch_raises():
    """Major mismatch: hard error with explicit upgrade link (D-05 UX)."""
    with pytest.raises(IncompatibleSchemaError, match=r"upgrade") as exc:
        check_compatibility("1.0.0", "2.0.0")
    assert "github.com" in str(exc.value)


def test_handshake_frame_extra_forbid():
    """Handshake itself is extra='forbid' so a future major breaks cleanly."""
    with pytest.raises(ValidationError):
        HandshakeFrame.model_validate(
            {
                "frame_type": "handshake",
                "schema_version": "1.0.0",
                "rogue_field": "x",
            }
        )


def test_telemetry_frame_lenient_ignores_unknown(valid_telemetry_payload):
    """Pitfall 6: lenient inbound model silently drops unknown fields from a newer sender."""
    result = TelemetryFrameLenient.model_validate(
        {**valid_telemetry_payload, "future_field_42": 99}
    )
    assert getattr(result, "future_field_42", None) is None


def test_make_handshake_uses_local_schema_version():
    """make_handshake() defaults schema_version to local SCHEMA_VERSION."""
    h = make_handshake()
    assert h.schema_version == SCHEMA_VERSION
    assert h.frame_type == "handshake"
    assert h.capabilities == []


def test_make_handshake_carries_capabilities():
    """capabilities= flag bag round-trips into HandshakeFrame."""
    h = make_handshake(capabilities=["bssid_raw_consent", "live_diagnose_v2"])
    assert h.capabilities == ["bssid_raw_consent", "live_diagnose_v2"]
