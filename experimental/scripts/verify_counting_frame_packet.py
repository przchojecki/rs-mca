#!/usr/bin/env python3
"""Verify the exact counting-frame packet certificate."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/counting-frame/counting_frame.json")
V8_CERT_PATH = Path("experimental/data/certificates/v8-ledger/v8_ledger.json")
NONCONTAIN_CERT_PATH = Path(
    "experimental/data/certificates/noncontain-degeneracy/noncontain_degeneracy.json"
)

SAMPLES = [
    {"n": 8, "j": 3, "locator_count": 56},
    {"n": 16, "j": 4, "locator_count": 1820},
    {"n": 32, "j": 5, "locator_count": 201376},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_local_dependency(path: Path, node: str) -> dict[str, Any]:
    require(path.exists(), f"missing dependency certificate: {path}")
    cert = json.loads(path.read_text())
    require(cert.get("source_dag_node") == node, f"dependency node mismatch for {path}")
    require(cert.get("status") == "PROVED", f"dependency is not PROVED: {node}")
    return cert


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.counting_frame.v1",
        "status": "PROVED",
        "source_dag_node": "counting_frame",
        "source_dag_dependencies": {
            "local": ["v8_ledger", "noncontain_degeneracy"],
            "external_prs": [{"node": "vtdv", "pr": 317, "branch": "codex/vendor-vtdv-fm1"}],
            "upstream_existing": ["f1_pencil_nf"],
        },
        "verdict": "finite_noncontained_slope_events_inject_into_the_locator_divisor_set",
        "claim": {
            "finite_locator_set": "binom(n,j) squarefree degree-j divisors/support complements",
            "fixed_locator_pencil": "A + z B = 0",
            "degenerate_removal": "A = B = 0 is removed by noncontain_degeneracy",
            "one_slope_rule": "after degenerate removal, v8_ledger gives <=1 finite slope per locator",
            "frame_consequence": "finite noncontained slope events inject into the finite locator set",
        },
        "sample_arithmetic": SAMPLES,
        "consumers": ["mca_safe"],
        "non_claims": [
            "does not count root tables for the F_17^32 M3/M4 window",
            "does not classify locators as tangent, quotient, extension, or aperiodic",
            "depends on the VTDV factorization packet in PR #317",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    v8 = validate_local_dependency(V8_CERT_PATH, "v8_ledger")
    noncontain = validate_local_dependency(NONCONTAIN_CERT_PATH, "noncontain_degeneracy")
    require("at_most_one" in v8.get("verdict", "") or "<=1" in str(v8), "V8 one-slope boundary missing")
    require("all_slope" in noncontain.get("verdict", ""), "noncontainment all-slope boundary missing")
    for row in cert["sample_arithmetic"]:
        got = comb(row["n"], row["j"])
        require(got == row["locator_count"], f"locator count mismatch: {row} != {got}")
    external = cert["source_dag_dependencies"]["external_prs"]
    require(external == [{"node": "vtdv", "pr": 317, "branch": "codex/vendor-vtdv-fm1"}], "VTDV PR dependency mismatch")


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
        print("PASS: counting_frame packet")


if __name__ == "__main__":
    main()
