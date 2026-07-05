#!/usr/bin/env python3
"""Verify the clique_cap packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/clique-cap/clique_cap.json")
SAMPLES = [
    {"m": 2, "a": 8, "k": 4, "n_min": 20, "edges": 4},
    {"m": 3, "a": 8, "k": 4, "n_min": 40, "edges": 9},
    {"m": 4, "a": 8, "k": 4, "n_min": 68, "edges": 16},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sample_row(m: int, a: int, k: int) -> dict[str, int]:
    return {"m": m, "a": a, "k": k, "n_min": k + m * m * (a - k), "edges": m * m}


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.clique_cap.v1",
        "status": "PROVED",
        "source_dag_node": "clique_cap",
        "verdict": "kmm_clique_amplification_requires_n_ge_k_plus_m2_slack",
        "formula": {
            "cap": "n >= k + m^2(a-k)",
            "equivalent": "m^2 <= (n-k)/(a-k)",
            "cell_disjointness": "the m^2 cross cells are disjoint outside the common k-set",
        },
        "sample_designs": SAMPLES,
        "upstream_evidence": [
            "experimental/scripts/verify_x1_clique_cap.py",
            "experimental/notes/x1/x1_deep_point_interleaved_bridge.md",
            "experimental/notes/roadmaps/proof_sketch/s7_list_side.md",
        ],
        "consumers": ["m_sweep", "m_handling"],
        "non_claims": [
            "does not prove list_safe",
            "does not prove an L1 image-fiber bound",
            "does not rule out all non-clique interleaved amplification mechanisms",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    for row in cert["sample_designs"]:
        got = sample_row(row["m"], row["a"], row["k"])
        require(row == got, f"sample arithmetic mismatch: {row} != {got}")
    require("m_sweep" in cert["consumers"], "m_sweep consumer missing")
    require("n >= k + m^2(a-k)" in cert["formula"]["cap"], "cap formula missing")


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
        print("PASS: clique_cap packet")


if __name__ == "__main__":
    main()
