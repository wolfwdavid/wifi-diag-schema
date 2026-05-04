"""TelemetryFrame + PingContinuity — the wire-format privacy contract.

The field allowlist on TelemetryFrame IS the privacy posture. Adding a field
requires updating tests/test_telemetry_field_allowlist.py AND adding a
why-allowlisted justification in _justifications.py (Pitfall 1).
"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from . import _justifications as J
from .enums import (
    OS,
    AuthEventClass,
    BssidMode,
    DhcpEventClass,
    DriverState,
    MacRandomizationState,
    NetworkMode,
)


class PingContinuity(BaseModel):
    """Ping continuity sub-frame: outbound RTT health over a sub-window.

    Aggregated client-side from `icmplib.async_ping()` (agent), so the wire
    format carries summary stats only — no raw probe sequence.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    window_ms: Annotated[int, Field(
        ge=0,
        description="Sub-window over which the ping stats were aggregated.",
    )]
    avg_rtt_ms: Annotated[float | None, Field(
        ge=0,
        default=None,
        description="Average ICMP echo RTT in milliseconds; None if no probes returned.",
    )]
    packet_loss_pct: Annotated[float, Field(
        ge=0.0,
        le=100.0,
        description="Percentage of probes lost in the sub-window (0-100).",
    )]
    jitter_ms: Annotated[float | None, Field(
        ge=0,
        default=None,
        description="Standard deviation of returned RTTs in milliseconds.",
    )]


class TelemetryFrame(BaseModel):
    """One window of telemetry. Field list IS the privacy contract.

    NEVER add: raw_message, username, eap_identity, cert_subject_dn,
               cert_bytes, password, radius_secret, packet_payload.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    # D-02 core 14
    timestamp: Annotated[float, Field(
        description="why-allowlisted: required for sequencing.",
    )]
    os: Annotated[OS, Field(
        description="why-allowlisted: per-OS class enablement (CLASS-04).",
    )]
    network_mode: Annotated[NetworkMode, Field(
        description="why-allowlisted: gates which classes apply.",
    )]
    rssi_dbm: Annotated[int, Field(
        ge=-100,
        le=0,
        description="why-allowlisted: primary RF feature.",
    )]
    bssid: Annotated[str, Field(
        pattern=r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$|^[0-9a-f]{64}$",
        description=J.BSSID,
    )]
    bssid_mode: Annotated[BssidMode, Field(
        description=(
            "why-allowlisted: disambiguates bssid format (raw MAC vs SHA-256 hash) "
            "per D-03 + RESEARCH Open Question 2."
        ),
    )]
    channel: Annotated[int, Field(
        ge=1,
        le=233,
        description="why-allowlisted: 2.4/5/6 GHz interference inference.",
    )]
    ping_continuity: Annotated[PingContinuity, Field(
        description=(
            "why-allowlisted: outbound ICMP continuity stats are the dominant "
            "continuity signal."
        ),
    )]
    latency_jitter_ms: Annotated[float | None, Field(
        ge=0,
        default=None,
        description="why-allowlisted: jitter is a continuity-disruption signal.",
    )]
    dns_resolution_ms: Annotated[float | None, Field(
        ge=0,
        default=None,
        description="why-allowlisted: DNS health is the dns_resolver_fail class signal.",
    )]
    dhcp_event_class: Annotated[DhcpEventClass, Field(
        description="why-allowlisted: dhcp_lease_churn class signal.",
    )]
    auth_event_class: Annotated[AuthEventClass, Field(
        description="why-allowlisted: 802.1X/RADIUS/EAP class signal.",
    )]
    captive_portal_detected: Annotated[bool, Field(
        description="why-allowlisted: captive_portal_expiry class signal.",
    )]
    mac_randomization_state: Annotated[MacRandomizationState, Field(
        description="why-allowlisted: mac_randomization_reject class signal.",
    )]
    driver_state: Annotated[DriverState, Field(
        description="why-allowlisted: driver_power_save_wake class signal.",
    )]

    # D-01 extended 4 (graceful absence per Pitfall 5 — None when not collected)
    per_packet_retry_count: Annotated[int | None, Field(
        ge=0,
        default=None,
        description=J.PER_PACKET_RETRY_COUNT,
    )]
    rts_cts_rate: Annotated[float | None, Field(
        ge=0,
        le=1,
        default=None,
        description=J.RTS_CTS_RATE,
    )]
    beacon_rssi_dbm: Annotated[int | None, Field(
        ge=-100,
        le=0,
        default=None,
        description=J.BEACON_RSSI_DBM,
    )]
    neighbor_ap_count_5ghz: Annotated[int | None, Field(
        ge=0,
        default=None,
        description=J.NEIGHBOR_AP_COUNT_5GHZ,
    )]

    # Meta (D-04)
    window_ms: Annotated[Literal[30000, 120000], Field(
        description=(
            "why-allowlisted: classifier needs to know its input window length "
            "(short for fast events, long for slow events). Surfaced as a feature."
        ),
    )]


class TelemetryFrameLenient(TelemetryFrame):
    """Inbound-only variant for minor-mismatch sessions (Pitfall 6 mitigation).

    Use on the RECEIVE side when `check_compatibility` returned `'minor_drift'`.
    The strict `TelemetryFrame` is still used for outbound construction; this
    lenient variant lets the receiver gracefully ignore fields a newer sender
    has added in a minor-version bump.

    Subclassing TelemetryFrame and overriding `model_config` is the documented
    Pydantic v2 pattern for variant configs without re-declaring fields.
    """

    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
        str_strip_whitespace=True,
    )
