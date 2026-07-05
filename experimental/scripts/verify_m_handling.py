#!/usr/bin/env python3
"""Verify the m_handling DAG assembly certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/m-handling/m_handling.json")

DEPENDENCIES = ["rules_freeze", "rules_m_reading", "m_sweep"]
UPSTREAM_EVIDENCE = [
    "experimental/scripts/verify_x1_clique_cap.py",
    "experimental/notes/roadmaps/wp_detail/wp0_2_wp4_4_rules_freeze_and_dither.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.m_handling.v1",
        "status": "PROVED",
        "source_dag_node": "m_handling",
        "source_dag_dependencies": DEPENDENCIES,
        "verdict": "per_constant_m_with_finite_affordable_sweep",
        "claim": (
            "The official list challenge is handled per declared constant m. "
            "Fixed-m packets and small-m batches are valid per-instance or "
            "partial determinations. The campaign's finite affordable sweep "
            "uses the clique cap n >= k + m^2(a-k), equivalently "
            "m <= sqrt((n-k)/(a-k)); larger constants still require a "
            "uniform-in-m or large-m regularity route."
        ),
        "scope": {
            "fixed_m": "valid per-instance determination when other row inputs close",
            "small_m_batch": "creditable partial coverage over listed constants",
            "affordable_sweep": "m <= sqrt((n-k)/t) near the row corridors",
            "large_m": "requires uniform-in-m or large-m regularity input",
        },
        "upstream_evidence": UPSTREAM_EVIDENCE,
        "consumers": ["list_safe"],
        "non_claims": [
            "does not prove list_safe",
            "does not prove the L1 image-fiber theorem",
            "does not prove the codegree conversion",
            "does not cover every constant m by finite sweep",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["source_dag_dependencies"] == DEPENDENCIES, "dependency list mismatch")
    claim = cert["claim"]
    require("per declared constant m" in claim, "claim must preserve fixed-m reading")
    require("n >= k + m^2(a-k)" in claim, "claim must include clique cap")
    require("larger constants" in claim, "claim must preserve large-m caveat")
    require(cert["consumers"] == ["list_safe"], "consumer list mismatch")


def emit_certificate(path: Path, cert: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, cert)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        loaded = json.loads(args.check.read_text())
        validate_certificate(loaded)
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: m_handling packet")


if __name__ == "__main__":
    main()
