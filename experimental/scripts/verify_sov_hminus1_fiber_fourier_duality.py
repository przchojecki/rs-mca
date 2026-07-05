#!/usr/bin/env python3
"""Replay the SOV h-minus-1 fiber Fourier-duality packet."""

from __future__ import annotations

import argparse
import cmath
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "sov" / "sov_hminus1_fiber_fourier_duality.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "sov-hminus1-fiber-fourier-duality"
    / "sov_hminus1_fiber_fourier_duality.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "sov_hminus1_fiber_fourier_duality",
    "coefficient_map": "c(L) = [X^{h-1}]L",
    "orthogonality": "1_{u=0} = |F|^{-1}",
    "non_claim": "does not bound the",
}


def character(q: int, x: int) -> complex:
    return cmath.exp(2j * math.pi * (x % q) / q)


def fourier_check() -> dict[str, Any]:
    q = 7
    values = [(i * i + 3 * i + 1) % q for i in range(31)]
    counts = Counter(values)
    sums = {xi: sum(character(q, xi * value) for value in values) for xi in range(q)}

    rows = []
    for a in range(q):
        reconstructed = sum(character(q, -xi * a) * sums[xi] for xi in range(q)) / q
        rows.append(
            {
                "a": a,
                "count": counts[a],
                "reconstructed": round(reconstructed.real),
                "imag_abs": abs(reconstructed.imag),
            }
        )

    fourier_bound = len(values) / q + sum(abs(sums[xi]) for xi in range(1, q)) / q
    return {
        "field_size": q,
        "sample_size": len(values),
        "rows": rows,
        "reconstruction_passed": all(row["count"] == row["reconstructed"] and row["imag_abs"] < 1e-9 for row in rows),
        "max_fiber": max(counts.values()),
        "fourier_bound_rounded": round(fourier_bound, 9),
        "bound_passed": max(counts.values()) <= fourier_bound + 1e-9,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "sov-hminus1-fiber-fourier-duality-v1",
        "status": "PROVED_FOURIER_DUALITY_REPLAY",
        "source_dag_node": "sov_hminus1_fiber_fourier_duality",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "fourier_check": fourier_check(),
        "non_claims": ["does not bound the actual SOV anchored-core character sums"],
        "note": "experimental/notes/sov/sov_hminus1_fiber_fourier_duality.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "sov-hminus1-fiber-fourier-duality-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["fourier_check"]
    if not (check["reconstruction_passed"] and check["bound_passed"]):
        raise AssertionError(f"failed Fourier check: {check}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['fourier_check']}")


if __name__ == "__main__":
    main()
