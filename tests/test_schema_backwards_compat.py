"""SCHEMA-04 regression gate: prove v1.1.0 payloads deserialize cleanly under v1.2.0.

Frozen fixtures in tests/fixtures/v1_1_0/ are byte-frozen captures of Verdict + TelemetryFrame
as serialized at v1.1.0 (Phase 8 plan 08-01 Task 1). Loading them with the v1.2.0 schema
proves backwards-compat. Forward-compat (v1.2.0-only fields) also asserted.

Per Phase 8 CONTEXT.md D-13 + RESEARCH §"Pattern 5".
"""
from __future__ import annotations

import json
from pathlib import Path

from wifi_diag_schema import (
    EvidenceItem,
    SCHEMA_VERSION,
    TelemetryFrame,
    Verdict,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "v1_1_0"


def test_schema_version_is_1_2_0():
    """Sentinel: prevents accidental version drift in this gating test."""
    assert SCHEMA_VERSION == "1.2.0", (
        f"SCHEMA_VERSION must be '1.2.0' at Phase 8; got {SCHEMA_VERSION!r}. "
        f"If you're rolling back, the fixtures + tests in this file are no longer valid."
    )


def test_v1_1_0_verdict_loads_under_v1_2_0():
    """SCHEMA-04: v1.1.0 serialized Verdict (no counter_evidence key) loads cleanly under v1.2.0."""
    src = (FIXTURE_DIR / "verdict.json").read_text(encoding="utf-8")
    # Sanity: raw JSON must NOT have counter_evidence (otherwise fixture is stale)
    raw = json.loads(src)
    assert "counter_evidence" not in raw, (
        f"Fixture verdict.json contains 'counter_evidence' — fixture is no longer a v1.1.0 capture. "
        f"Regenerate from v1.1.0 tag and re-commit. Current keys: {list(raw.keys())}"
    )
    assert raw.get("schema_version") == "1.1.0", (
        f"Fixture must claim schema_version='1.1.0' to prove cross-version load; got {raw.get('schema_version')!r}"
    )
    # Load under v1.2.0 schema
    v = Verdict.model_validate_json(src)
    assert v.schema_version == "1.1.0", (
        f"Loaded Verdict.schema_version must preserve fixture value ('1.1.0'); got {v.schema_version!r}"
    )
    assert v.counter_evidence == [], (
        f"counter_evidence must adopt default_factory=list ([]) when absent from v1.1.0 payload; got {v.counter_evidence!r}"
    )


def test_v1_1_0_telemetry_loads_under_v1_2_0():
    """SCHEMA-04: prove no inadvertent breakage to TelemetryFrame (Phase 8 doesn't touch it)."""
    src = (FIXTURE_DIR / "telemetry_frame.json").read_text(encoding="utf-8")
    t = TelemetryFrame.model_validate_json(src)
    assert t.os in ("windows", "macos", "linux"), f"TelemetryFrame.os unexpected: {t.os!r}"
    assert t.bssid_mode == "hashed", f"TelemetryFrame.bssid_mode unexpected: {t.bssid_mode!r}"


def test_v1_2_0_verdict_with_counter_evidence_roundtrips():
    """SCHEMA-02 forward-compat: a v1.2.0 producer can emit non-empty counter_evidence."""
    v = Verdict(
        top_class="dns_resolver_fail",
        confidence=0.87,
        top_k=[("dns_resolver_fail", 0.87), ("isp_upstream_fail", 0.10)],
        headline="DNS resolver returned SERVFAIL for example.com",
        suggested_fix="Switch DNS to 1.1.1.1 or 8.8.8.8 temporarily.",
        evidence=[EvidenceItem(telemetry_path="dns_resolution_ms", claim="DNS lookup timeout 5000ms.")],
        counter_evidence=[
            EvidenceItem(
                telemetry_path="ping_continuity.packet_loss_pct",
                claim="0% packet loss argues against ISP upstream outage.",
            ),
        ],
    )
    blob = v.model_dump_json()
    v2 = Verdict.model_validate_json(blob)
    assert len(v2.counter_evidence) == 1, f"counter_evidence length: {len(v2.counter_evidence)}"
    assert v2.counter_evidence[0].telemetry_path == "ping_continuity.packet_loss_pct"


def test_unknown_disconnect_class_accepted():
    """SCHEMA-01: 'unknown' is a valid DisconnectClass at v1.2.0."""
    v = Verdict(
        top_class="unknown",
        confidence=0.0,
        top_k=[("unknown", 0.0)],
        headline="Insufficient evidence for confident attribution",
        suggested_fix="Collect more telemetry over a longer window and re-diagnose.",
        evidence=[],
    )
    assert v.top_class == "unknown"
    # And: it round-trips through JSON
    blob = v.model_dump_json()
    v2 = Verdict.model_validate_json(blob)
    assert v2.top_class == "unknown"


def test_counter_evidence_defaults_to_empty_list_not_shared_mutable():
    """Pitfall 4 guard: default_factory=list, not default=[]. Two Verdicts must NOT share a list."""
    v1 = Verdict(
        top_class="unknown", confidence=0.0, top_k=[("unknown", 0.0)],
        headline="x", suggested_fix="y", evidence=[],
    )
    v2 = Verdict(
        top_class="unknown", confidence=0.0, top_k=[("unknown", 0.0)],
        headline="x", suggested_fix="y", evidence=[],
    )
    # frozen=True prevents mutation, but identity check still proves separate instantiation
    assert v1.counter_evidence is not v2.counter_evidence or v1.counter_evidence == [], (
        "counter_evidence defaults must not be shared mutable state (Pitfall 4)"
    )
