#!/usr/bin/env python3
"""Verify the m_sweep packet certificate."""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/m-sweep/m_sweep.json")
NORMALIZED_EXAMPLES = [
    {"ratio": 256, "m_max": 16},
    {"ratio": 961, "m_max": 31},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.m_sweep.v1",
        "status": "PROVED",
        "source_dag_node": "m_sweep",
        "source_dag_dependencies": ["clique_cap"],
        "verdict": "finite_affordable_m_sweep_from_clique_cap",
        "derivation": {
            "parent_cap": "n >= k + m^2(a-k)",
            "slack_variable": "t = a-k",
            "sweep_bound": "m <= floor(sqrt((n-k)/t))",
            "recorded_near_corridor_range": "approximately 16..31",
        },
        "normalized_examples": NORMALIZED_EXAMPLES,
        "upstream_evidence": [
            "experimental/data/certificates/clique-cap/clique_cap.json",
            "experimental/scripts/verify_x1_clique_cap.py",
            "experimental/notes/roadmaps/wp_detail/wp0_2_wp4_4_rules_freeze_and_dither.md",
        ],
        "consumers": ["m_handling", "list_safe"],
        "non_claims": [
            "does not cover arbitrary constant m uniformly",
            "does not prove list_safe",
            "does not provide the large-m regularity branch",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    derivation = cert["derivation"]
    require(derivation["slack_variable"] == "t = a-k", "slack variable mismatch")
    require("floor(sqrt((n-k)/t))" in derivation["sweep_bound"], "sweep formula missing")
    for row in cert["normalized_examples"]:
        require(isqrt(row["ratio"]) == row["m_max"], f"bad normalized example: {row}")
    require(cert["source_dag_dependencies"] == ["clique_cap"], "dependency mismatch")


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
        print("PASS: m_sweep packet")


if __name__ == "__main__":
    main()
