#!/usr/bin/env python3
"""Replay the L1 petal squarefree counting-soundness certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "l1-petal-squarefree-classification-counting-soundness"
    / "l1_petal_squarefree_classification_counting_soundness.json"
)
NOTE = (
    REPO
    / "experimental"
    / "notes"
    / "l1"
    / "l1_petal_squarefree_classification_counting_soundness.md"
)


ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "petal_squarefree_classification_counting_soundness",
    "max_exponent": "A = max_i A_i",
    "sum_constant": "B = sum_i B_i",
    "union_bound": "sum_i |C_i| <= sum_i B_i n^{A_i} <= (sum_i B_i) n^A",
    "non_claim": "does not construct the squarefree classification ledger",
}


def class_sum(classes: list[tuple[int, int]], n: int) -> int:
    return sum(coefficient * (n**exponent) for coefficient, exponent in classes)


def combined_bound(classes: list[tuple[int, int]], n: int) -> int:
    exponent = max(exponent for _, exponent in classes)
    coefficient = sum(coefficient for coefficient, _ in classes)
    return coefficient * (n**exponent)


def sample_checks() -> list[dict[str, Any]]:
    samples = [
        [(2, 3), (5, 1), (7, 3)],
        [(1, 0), (4, 2), (9, 1), (3, 4)],
        [(11, 0)],
    ]
    checks = []
    for classes in samples:
        for n in (1, 2, 17, 101):
            lhs = class_sum(classes, n)
            rhs = combined_bound(classes, n)
            checks.append(
                {
                    "classes": [list(item) for item in classes],
                    "n": n,
                    "class_sum": lhs,
                    "combined_bound": rhs,
                    "passes": lhs <= rhs,
                }
            )
    return checks


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "l1-petal-squarefree-classification-counting-soundness-v1",
        "status": "PROVED_FINITE_UNION_COUNTING",
        "source_dag_node": "petal_squarefree_classification_counting_soundness",
        "statement": (
            "a finite uncharged squarefree classification with c-independent "
            "class exponents has a c-independent polynomial union bound"
        ),
        "anchor_checks": checks,
        "sample_checks": sample_checks(),
        "dependencies": ["finite-union polynomial counting"],
        "non_claims": [
            "does not construct the squarefree classification ledger",
            "does not prove that every kernel locator is covered by a ledger",
            "does not close the L1 mixed/growing residual by itself",
        ],
        "note": "experimental/notes/l1/l1_petal_squarefree_classification_counting_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "l1-petal-squarefree-classification-counting-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_samples = [check for check in cert["sample_checks"] if not check["passes"]]
    if failed_samples:
        raise AssertionError(f"failed sample checks: {failed_samples}")
    if "c-independent" not in cert["statement"]:
        raise AssertionError("statement must record c-independent exponent")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1-petal-squarefree-classification-counting-soundness certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print(f"  sample checks: {len(cert['sample_checks'])}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
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
        print_summary(cert)


if __name__ == "__main__":
    main()
