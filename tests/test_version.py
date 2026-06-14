"""Phase 3 plan 03-01 / Pitfall D defense: SCHEMA_VERSION matches pyproject.

Single source of truth: the constant in ``version.py`` and the version under
``[project]`` in ``pyproject.toml`` must agree. Tag-time CI publishes from
pyproject; runtime code reads SCHEMA_VERSION; drift between the two would
silently ship a v1.1.0 wheel reporting v1.0.0 (or vice versa).
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from wifi_diag_schema.version import SCHEMA_VERSION


def test_schema_version_matches_pyproject() -> None:
    pyp_path = Path(__file__).parent.parent / "pyproject.toml"
    pyp = tomllib.loads(pyp_path.read_text())
    assert SCHEMA_VERSION == pyp["project"]["version"]
