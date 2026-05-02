# wifi-diag-schema

**Privacy contract: the field allowlist on `TelemetryFrame` is the privacy posture. There is no `raw_message`, no `username`, no credential field — by construction.**

The wire-format Pydantic schema for the [AI Internet Diagnostic](https://github.com/WolfDavid/ai-internet-diagnostic-space) project. The cross-platform local agent, the Hugging Face Space UI, and the trained model artifact all `pip install wifi-diag-schema==X.Y.Z` and operate against the same set of typed contracts.

The schema source IS the privacy policy. Adding a field is a deliberate, reviewable act — the test suite enforces a literal allowlist regression gate (`tests/test_telemetry_field_allowlist.py`), and `pydantic.ConfigDict(extra="forbid")` rejects any unknown field at validation time.

## Install

```bash
pip install wifi-diag-schema==1.0.0
```

## Usage

```python
from pydantic import ValidationError
from wifi_diag_schema import TelemetryFrame, Verdict, EvidenceItem, SCHEMA_VERSION

# Attempt to set a field outside the allowlist → ValidationError("extra_forbidden")
try:
    TelemetryFrame.model_validate({"raw_message": "anything"})
except ValidationError as e:
    print(e)  # extra_forbidden — the privacy contract spoke
```

## Schema fields (v1.0.0)

| Group | Count | Notes |
|---|---|---|
| Core (D-02) | 14 | timestamp, os, network_mode, rssi_dbm, bssid, channel, ping_continuity, latency_jitter_ms, dns_resolution_ms, dhcp_event_class, auth_event_class, captive_portal_detected, mac_randomization_state, driver_state |
| Extended (D-01) | 4 | per_packet_retry_count, rts_cts_rate, beacon_rssi_dbm, neighbor_ap_count_5ghz |
| Privacy mode | 1 | bssid_mode (raw \| hashed) |
| Meta | 1 | window_ms |
| **Total** | **20** | |

Every field carries a `why-allowlisted` justification in its `Field(description=...)`. See `src/wifi_diag_schema/_justifications.py` for the extended-field rationale and per-OS source confidence tiers.

## Versioning

Strict SemVer (D-05):
- **Major** = breaking change (field removed, type narrowed, validator tightened)
- **Minor** = additive (new optional field with default; new enum value)
- **Patch** = doc-only

The agent and Space exchange `schema_version` via `HandshakeFrame` on the first SSE message of every live session (added in plan 01-02). Major mismatch → hard error. Minor mismatch → warn-but-continue.

## Release

Tag a release as `vX.Y.Z`; the `publish.yml` workflow runs OIDC Trusted Publishing automatically. The Trusted Publisher must be registered at <https://pypi.org/manage/account/publishing/> pointing at this repo + the `publish.yml` workflow filename.

## License

Apache-2.0.
