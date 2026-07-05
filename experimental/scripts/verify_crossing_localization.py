#!/usr/bin/env python3
"""Replay the MCA crossing-localization packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "crossing_localization.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "crossing-localization"
    / "crossing_localization.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "crossing_localization",
    "staircase": "nonincreasing",
    "adjacent_crossing": "B_C(a* - 1) > B* >= B_C(a*)",
    "candidate_bound": "ceil(w) + 1",
    "non_claim": "does not prove the pointwise safe upper certificate",
}


def is_nonincreasing(values: list[int]) -> bool:
    return all(left >= right for left, right in zip(values, values[1:]))


def first_safe_index(staircase: dict[int, int], threshold: int, lo: int, hi: int) -> int:
    for index in range(lo, hi + 1):
        if staircase[index] <= threshold:
            return index
    raise AssertionError("bracket does not contain a safe index")


def interval_integer_count(left: float, right: float) -> int:
    return max(0, math.floor(right) - math.ceil(left) + 1)


def toy_check() -> dict[str, object]:
    staircase = {
        10: 14,
        11: 11,
        12: 7,
        13: 7,
        14: 4,
    }
    threshold = 7
    lo = 11
    hi = 14
    first_safe = first_safe_index(staircase, threshold, lo, hi)
    real_left = 11.3
    real_right = 13.1
    width = real_right - real_left
    candidate_count = interval_integer_count(real_left, real_right)

    values = [staircase[index] for index in sorted(staircase)]
    return {
        "staircase": {str(key): value for key, value in staircase.items()},
        "threshold": threshold,
        "nonincreasing": is_nonincreasing(values),
        "bracket": {
            "a_lo": lo,
            "a_hi": hi,
            "unsafe_before_lo": staircase[lo - 1] > threshold,
            "safe_at_hi": staircase[hi] <= threshold,
        },
        "first_safe": first_safe,
        "adjacent_crossing_holds": staircase[first_safe - 1] > threshold
        and threshold >= staircase[first_safe],
        "real_corridor": {
            "left": real_left,
            "right": real_right,
            "width": width,
            "integer_count": candidate_count,
            "ceil_width_plus_one": math.ceil(width) + 1,
            "count_bound_holds": candidate_count <= math.ceil(width) + 1,
        },
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "crossing-localization-v1",
        "status": "PROVED",
        "source_dag_node": "crossing_localization",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove the pointwise safe upper certificate",
            "does not prove the unsafe lower certificate",
            "does not prove a row-level adjacent theorem",
        ],
        "note": "experimental/notes/thresholds/crossing_localization.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "crossing-localization-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    if not toy.get("nonincreasing"):
        raise AssertionError("staircase monotonicity failed")
    bracket = toy["bracket"]
    if not isinstance(bracket, dict) or not (
        bracket.get("unsafe_before_lo") and bracket.get("safe_at_hi")
    ):
        raise AssertionError("bracket check failed")
    if not toy.get("adjacent_crossing_holds"):
        raise AssertionError("adjacent crossing check failed")
    corridor = toy["real_corridor"]
    if not isinstance(corridor, dict) or not corridor.get("count_bound_holds"):
        raise AssertionError("corridor count bound failed")


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
