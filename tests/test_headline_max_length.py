"""Phase 3 plan 03-01 / D-VERDICT-06: Verdict.headline max_length=140.

Anthropic Structured Outputs respects Pydantic ``Field(max_length=...)``
constraints, so a 140-char ceiling enforced in the schema is enforced at
generation time. Casual visitors and IT-ticket exports both render cleanly.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from wifi_diag_schema.verdict import Verdict

_BASE: dict = dict(
    top_class="auth_8021x_eap_fail",
    confidence=0.9,
    top_k=[("auth_8021x_eap_fail", 0.9)],
    suggested_fix="x",
    evidence=[],
)


def test_headline_140_passes() -> None:
    Verdict(headline="x" * 140, **_BASE)


def test_headline_141_raises() -> None:
    with pytest.raises(ValidationError):
        Verdict(headline="x" * 141, **_BASE)
