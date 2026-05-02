"""Verdict + EvidenceItem — output schema for the LLM narrator (Phase 3).

Round-tripped through Anthropic Structured Outputs via Verdict.model_json_schema().
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .enums import DisconnectClass
from .version import SCHEMA_VERSION


class EvidenceItem(BaseModel):
    """One citation in the narrator's evidence drill-down."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    telemetry_path: Annotated[str, Field(
        description=(
            "Dotted path into TelemetryFrame, e.g. 'rssi_dbm' or "
            "'ping_continuity.packet_loss_pct'. Validated against actual telemetry "
            "by the citation guardrail (LLM-03, Phase 3)."
        ),
    )]
    claim: Annotated[str, Field(
        description="Plain-English claim grounded in the cited telemetry value.",
    )]
    attribution: Annotated[dict | None, Field(
        default=None,
        description=(
            "Reserved for v2 SHAP attribution payloads (CLASS-V2-02). "
            "Phase 1 schema accepts the field; Phase 1 production code leaves it None."
        ),
    )]


class Verdict(BaseModel):
    """Diagnostic verdict — top-K classifier output + LLM narration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Annotated[str, Field(
        default=SCHEMA_VERSION,
        description="Wire-format version (D-13 release pinning).",
    )]
    top_class: Annotated[DisconnectClass, Field(
        description="Highest-confidence disconnect class (one of the 10 canonical slugs).",
    )]
    confidence: Annotated[float, Field(
        ge=0.0,
        le=1.0,
        description=(
            "Calibrated confidence in top_class (CLASS-02; populated by "
            "CalibratedClassifierCV in Phase 2)."
        ),
    )]
    top_k: Annotated[list[tuple[DisconnectClass, float]], Field(
        description=(
            "Top-K (class, prob) pairs ordered by descending probability "
            "(CLASS-03 — UI shows alternatives)."
        ),
    )]
    headline: Annotated[str, Field(
        description="Plain-English diagnosis (LLM-04).",
    )]
    suggested_fix: Annotated[str, Field(
        description="Plain-English remediation (LLM-04).",
    )]
    evidence: Annotated[list[EvidenceItem], Field(
        description="Citations grounded in TelemetryFrame paths (LLM-02, LLM-03).",
    )]
