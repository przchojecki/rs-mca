#!/usr/bin/env python3
"""Replay the Hankel moment-clean leaves packet."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_moment_clean_leaves.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-moment-clean-leaves"
    / "hankel_moment_clean_leaves.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "hankel_moment_clean_leaves",
    "pinned_variant": "pinned-value variant",
    "moment_bound": "sum_f binom(rho(f), s) <= binom(|E|, s) q^{dim A - s}",
    "non_claim": "rank-profile entropy bound",
}


def zero_moment(points: list[tuple[int, ...]], s: int) -> int:
    total = 0
    width = len(points[0])
    for point in points:
        zeros = sum(1 for value in point if value == 0)
        if zeros >= s:
            total += math.comb(zeros, s)
    return total


def toy_check() -> dict[str, object]:
    q = 5
    clean_points = [(a, b) for a in range(q) for b in range(q)]
    clean_dim = 2
    clean_s = 1
    clean_bound = math.comb(2, clean_s) * (q ** (clean_dim - clean_s))
    clean_moment = zero_moment(clean_points, clean_s)

    pinned_points = [(a, 1) for a in range(q)]
    pinned_dim = 1
    pinned_s = 1
    pinned_bound = math.comb(2, pinned_s) * (q ** (pinned_dim - pinned_s))
    pinned_moment = zero_moment(pinned_points, pinned_s)
    all_zero_missing = (0, 0) not in pinned_points

    onto_projection_counts = {
        str(value): sum(1 for point in clean_points if point[0] == value)
        for value in range(q)
    }
    pinned_projection_counts = {
        str(value): sum(1 for point in pinned_points if point[1] == value)
        for value in range(q)
    }

    return {
        "field": "F_5",
        "clean_case": {
            "point_count": len(clean_points),
            "dimension": clean_dim,
            "s": clean_s,
            "zero_moment": clean_moment,
            "moment_bound": clean_bound,
            "bound_is_sharp": clean_moment == clean_bound,
            "projection_fiber_counts": onto_projection_counts,
            "projection_onto": set(onto_projection_counts.values()) == {q},
        },
        "pinned_case": {
            "point_count": len(pinned_points),
            "dimension": pinned_dim,
            "s": pinned_s,
            "zero_moment": pinned_moment,
            "moment_bound": pinned_bound,
            "bound_holds": pinned_moment <= pinned_bound,
            "all_zero_missing": all_zero_missing,
            "pinned_coordinate_fiber_counts": pinned_projection_counts,
        },
        "subsets_checked": [
            list(subset) for subset in itertools.combinations(range(2), 1)
        ],
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-moment-clean-leaves-v1",
        "status": "PROVED",
        "source_dag_node": "hankel_moment_clean_leaves",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove rank-profile entropy",
            "does not prove full Hankel termination",
        ],
        "note": "experimental/notes/m1/hankel_moment_clean_leaves.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-moment-clean-leaves-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    if not toy["clean_case"]["bound_is_sharp"]:
        raise AssertionError("clean-case moment bound failed")
    if not toy["pinned_case"]["bound_holds"]:
        raise AssertionError("pinned-case moment bound failed")
    if not toy["pinned_case"]["all_zero_missing"]:
        raise AssertionError("pinned zero-missing check failed")


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
