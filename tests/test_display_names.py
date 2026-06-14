"""Phase 3 plan 03-01 / D-VERDICT-05: DISPLAY_NAMES dict on the schema.

The constant maps every canonical DisconnectClass slug to its plain-English
display label (e.g. ``auth_8021x_eap_fail`` -> ``"802.1X authentication failure"``).
Both the LLM narrator and the templated/no-LLM narrator (Phase 4 local-only mode)
read the same dict so the verdict UI label matches across rendering paths.
"""

from __future__ import annotations

from typing import get_args

from wifi_diag_schema.enums import DISPLAY_NAMES, DisconnectClass


def test_display_names_has_all_classes() -> None:
    slugs = set(get_args(DisconnectClass))
    assert set(DISPLAY_NAMES.keys()) == slugs, f"missing: {slugs - DISPLAY_NAMES.keys()}"
    for k, v in DISPLAY_NAMES.items():
        assert isinstance(v, str) and len(v) > 0, f"empty display name for {k}"


def test_display_names_keys_match_canonical_order() -> None:
    assert list(DISPLAY_NAMES.keys()) == list(get_args(DisconnectClass))


def test_display_names_includes_unknown_at_v1_2_0() -> None:
    """SCHEMA-01 / D-11: 'unknown' present with long-explicit phrasing."""
    from wifi_diag_schema.enums import DISPLAY_NAMES

    assert DISPLAY_NAMES.get("unknown") == "Insufficient evidence for confident attribution", (
        f"DISPLAY_NAMES['unknown'] must be the locked D-11 long-explicit phrasing; "
        f"got: {DISPLAY_NAMES.get('unknown')!r}"
    )
