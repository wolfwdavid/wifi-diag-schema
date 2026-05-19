# Changelog

All notable changes to `wifi-diag-schema` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to strict [Semantic Versioning](https://semver.org/) per the project's D-05 decision (major = breaking, minor = additive, patch = doc-only).

## [1.2.0] — 2026-05-19

### Added

- `DisconnectClass.unknown` (SCHEMA-01 / D-10) — 11th member, last position, for OOD abstention sentinel. Consumed by Phase 9 OOD classifier.
- `Verdict.counter_evidence: list[EvidenceItem] = []` (SCHEMA-02 / D-09) — defaults to empty list via `default_factory=list`. Consumed by Phase 12 narrator counter-evidence.
- `DISPLAY_NAMES["unknown"] = "Insufficient evidence for confident attribution"` (D-11) — long-explicit phrasing signalling OOD abstention semantics.

### Compatibility

- Backwards-compatible additive bump. Serialized v1.1.0 `Verdict` payloads deserialize cleanly under v1.2.0 (proven by `tests/test_schema_backwards_compat.py`); the absent `counter_evidence` field adopts its `default_factory=list` default.
- All `extra="forbid"` and `frozen=True` config preserved.

## [1.0.0] — Unreleased

### Added

- Initial schema.
- `TelemetryFrame` allowlist (18 core fields + 1 `bssid_mode` + 1 `window_ms` = 20 total per D-01).
- `Verdict` + `EvidenceItem` (Phase 3 LLM-narrator output schema; Anthropic Structured Outputs compatible).
- `HandshakeFrame` + `check_compatibility()` + `IncompatibleSchemaError` + `make_handshake()` (D-05; Phase 5 transport reuses this for the agent ↔ Space SSE channel).
- `TelemetryFrameLenient` (Pitfall 6 mitigation: inbound-side `extra='ignore'` parser for minor-version drift; the strict `TelemetryFrame` remains the outbound construction model).
