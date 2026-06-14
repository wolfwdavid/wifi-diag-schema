"""Schema-version handshake (D-05) — first SSE message of every live session.

Strict SemVer:
- major mismatch is a hard error with explicit upgrade-link UX
- minor mismatch warns loudly and returns "minor_drift" (Pitfall 3 mitigation:
  do not swallow drift silently — operators need to see the warning)
- patch mismatch is doc-only, returns "match" silently

Phase 5 transport reuses this exact handshake on the agent <-> Space SSE channel.
"""

from __future__ import annotations

import warnings
from typing import Literal

from packaging.version import Version
from pydantic import BaseModel, ConfigDict, Field

from .version import SCHEMA_VERSION

_UPGRADE_URL = "https://github.com/WolfDavid/wifi-diag-schema/releases"


class HandshakeFrame(BaseModel):
    """First-frame negotiation payload exchanged between agent and Space.

    `extra='forbid'` so a future major can break the handshake format cleanly
    (RESEARCH Pattern 3 design rule).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    frame_type: Literal["handshake"] = "handshake"
    schema_version: str  # SemVer string of the sender's wifi-diag-schema
    capabilities: list[str] = Field(
        default_factory=list,
        description=(
            "Forward-compat flag bag for additive capability negotiation "
            "(D-05 minor-add). Examples: 'bssid_raw_consent', 'live_diagnose_v2'."
        ),
    )


class IncompatibleSchemaError(RuntimeError):
    """Raised on major-version mismatch between agent and Space (D-05)."""


def check_compatibility(local: str, remote: str) -> Literal["match", "minor_drift"]:
    """Compare two SemVer strings per D-05 rules.

    Returns:
        "match"        — major+minor align (patch differences are silent).
        "minor_drift"  — same major, different minor; emits UserWarning.

    Raises:
        IncompatibleSchemaError — major version differs; message includes
        the explicit upgrade-link UX from D-05.
    """
    lv, rv = Version(local), Version(remote)
    if lv.major != rv.major:
        raise IncompatibleSchemaError(
            f"Schema major-version mismatch: local={local}, remote={remote}. "
            f"upgrade required: {_UPGRADE_URL}"
        )
    if lv.minor != rv.minor:
        warnings.warn(
            f"Schema minor-version mismatch: local={local} vs remote={remote}; "
            "continuing with intersection of features (newer side ignores "
            "unknown fields via TelemetryFrameLenient).",
            UserWarning,
            stacklevel=2,
        )
        return "minor_drift"
    return "match"


def make_handshake(capabilities: list[str] | None = None) -> HandshakeFrame:
    """Construct a HandshakeFrame stamped with the local SCHEMA_VERSION."""
    return HandshakeFrame(
        schema_version=SCHEMA_VERSION,
        capabilities=capabilities or [],
    )
