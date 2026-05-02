# Changelog

All notable changes to `wifi-diag-schema` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to strict [Semantic Versioning](https://semver.org/) per the project's D-05 decision (major = breaking, minor = additive, patch = doc-only).

## [1.0.0] — Unreleased

### Added

- Initial schema.
- `TelemetryFrame` allowlist (18 core fields + 1 `bssid_mode` + 1 `window_ms` = 20 total per D-01).
- `Verdict` + `EvidenceItem` (Phase 3 LLM-narrator output schema; Anthropic Structured Outputs compatible).
- `HandshakeFrame` (added in plan 01-02).
