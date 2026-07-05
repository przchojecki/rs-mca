#!/usr/bin/env python3
"""Replay the DLI circle log-integral constant packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_circle_log_integral_constant.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-circle-log-integral-constant"
    / "dli_circle_log_integral_constant.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_circle_log_integral_constant",
    "constant": "int_0^1 log |cos(2 pi x)|^2 dx = -2 log 2",
    "classical_integral": "int_0^{pi/2} log(cos u) du",
    "non_claim": "peak-mass estimate",
}


def midpoint_integral(samples: int) -> float:
    total = 0.0
    for i in range(samples):
        x = (i + 0.5) / samples
        c = abs(math.cos(2.0 * math.pi * x))
        total += math.log(c * c)
    return total / samples


def numerical_check() -> dict[str, Any]:
    samples = 200_000
    estimate = midpoint_integral(samples)
    target = -2.0 * math.log(2.0)
    return {
        "samples": samples,
        "estimate": estimate,
        "target": target,
        "absolute_error": abs(estimate - target),
        "tolerance": 2.0e-5,
        "within_tolerance": abs(estimate - target) < 2.0e-5,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-circle-log-integral-constant-v1",
        "status": "PROVED_CIRCLE_CONSTANT_REPLAY",
        "source_dag_node": "dli_circle_log_integral_constant",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "symbolic_constant": "-2*log(2)",
        "numerical_check": numerical_check(),
        "non_claims": [
            "does not prove equidistribution of DLI sequences",
            "does not prove peak-mass estimates",
        ],
        "note": "experimental/notes/dli/dli_circle_log_integral_constant.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-circle-log-integral-constant-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["numerical_check"]["within_tolerance"]:
        raise AssertionError(f"failed numerical check: {cert['numerical_check']}")


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
        print(f"{cert['status']}: {cert['numerical_check']}")


if __name__ == "__main__":
    main()
