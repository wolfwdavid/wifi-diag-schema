"""wifi-diag-schema — wire-format Pydantic schema for AI Internet Diagnostic.

The field allowlist on TelemetryFrame IS the privacy contract.
Adding a field requires updating tests/test_telemetry_field_allowlist.py
AND _justifications.py (Pitfall 1).
"""
from wifi_diag_schema.enums import (
    OS,
    AuthEventClass,
    BssidMode,
    DhcpEventClass,
    DisconnectClass,
    DriverState,
    MacRandomizationState,
    NetworkMode,
)
from wifi_diag_schema.telemetry import PingContinuity, TelemetryFrame
from wifi_diag_schema.verdict import EvidenceItem, Verdict
from wifi_diag_schema.version import SCHEMA_VERSION

# NOTE: HandshakeFrame, IncompatibleSchemaError, check_compatibility added by plan 01-02.

__all__ = [
    "SCHEMA_VERSION",
    "TelemetryFrame",
    "PingContinuity",
    "Verdict",
    "EvidenceItem",
    "OS",
    "NetworkMode",
    "AuthEventClass",
    "DhcpEventClass",
    "DriverState",
    "MacRandomizationState",
    "BssidMode",
    "DisconnectClass",
]
