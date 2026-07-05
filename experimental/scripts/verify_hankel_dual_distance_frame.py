#!/usr/bin/env python3
"""Replay the Hankel dual-distance frame packet."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_dual_distance_frame.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-dual-distance-frame"
    / "hankel_dual_distance_frame.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "f_dual_distance_frame",
    "dual_equivalence": "dual-code word",
    "minimal_support": "minimal supported dependence",
    "non_claim": "does not prove termination",
}


def mod_rank(rows: list[list[int]], p: int) -> int:
    matrix = [row[:] for row in rows if any(x % p for x in row)]
    if not matrix:
        return 0
    height = len(matrix)
    width = len(matrix[0])
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, height):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col] % p, -1, p)
        matrix[rank] = [(x * inv) % p for x in matrix[rank]]
        for row in range(height):
            if row == rank:
                continue
            factor = matrix[row][col] % p
            if factor:
                matrix[row] = [
                    (x - factor * y) % p for x, y in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == height:
            break
    return rank


def has_trace_dependence(eval_rows: list[list[int]], subset: Iterable[int], p: int) -> bool:
    traces = [eval_rows[i] for i in subset]
    return mod_rank(traces, p) < len(traces)


def has_dual_word(eval_rows: list[list[int]], subset: Iterable[int], p: int) -> bool:
    subset = list(subset)
    for coeffs in itertools.product(range(p), repeat=len(subset)):
        if not any(coeffs):
            continue
        sums = [0] * len(eval_rows[0])
        for coeff, idx in zip(coeffs, subset):
            for col, value in enumerate(eval_rows[idx]):
                sums[col] = (sums[col] + coeff * value) % p
        if all(value == 0 for value in sums):
            return True
    return False


def toy_check() -> dict[str, object]:
    p = 5
    domain = [0, 1, 2]
    # P = span(1, X), so each trace is the row [1, x].
    eval_rows = [[1, x % p] for x in domain]
    checked: list[dict[str, object]] = []
    all_match = True
    for size in [1, 2, 3]:
        for subset in itertools.combinations(range(len(domain)), size):
            dep = has_trace_dependence(eval_rows, subset, p)
            dual = has_dual_word(eval_rows, subset, p)
            checked.append({"subset": list(subset), "trace_dependent": dep, "dual_word": dual})
            all_match = all_match and dep == dual
    return {
        "field": "F_5",
        "flat": "span(1,X)",
        "domain": domain,
        "all_subsets_match": all_match,
        "two_point_subsets_independent": all(
            not record["trace_dependent"]
            for record in checked
            if len(record["subset"]) == 2
        ),
        "three_point_subset_dependent": any(
            record["trace_dependent"] for record in checked if len(record["subset"]) == 3
        ),
        "checked_subsets": checked,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-dual-distance-frame-v1",
        "status": "PROVED",
        "source_dag_node": "f_dual_distance_frame",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not classify Hankel sparse-dual supports",
            "does not prove descent termination",
        ],
        "note": "experimental/notes/m1/hankel_dual_distance_frame.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-dual-distance-frame-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    for key in [
        "all_subsets_match",
        "two_point_subsets_independent",
        "three_point_subset_dependent",
    ]:
        if not toy.get(key):
            raise AssertionError(f"failed toy check: {key}")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
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
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
