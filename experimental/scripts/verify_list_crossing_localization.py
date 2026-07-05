#!/usr/bin/env python3
"""Replay the list crossing-localization packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "list_crossing_localization.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "list-crossing-localization"
    / "list_crossing_localization.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "list_crossing_localization",
    "convention": "agreement-index convention",
    "nested": "Lambda(U, delta + 1) subset Lambda(U, delta)",
    "supremum": "L(delta) := sup_U |Lambda(U, delta)|",
    "adjacent": "L(delta* - 1) > eps |F| >= L(delta*)",
    "non_claim": "pointwise list upper certificate",
}


def nested_by_delta(lists_by_word: dict[str, dict[int, set[str]]]) -> bool:
    for by_delta in lists_by_word.values():
        deltas = sorted(by_delta)
        for left, right in zip(deltas, deltas[1:]):
            if not by_delta[right].issubset(by_delta[left]):
                return False
    return True


def supremum_staircase(lists_by_word: dict[str, dict[int, set[str]]]) -> dict[int, int]:
    deltas = sorted(next(iter(lists_by_word.values())))
    return {
        delta: max(len(by_delta[delta]) for by_delta in lists_by_word.values())
        for delta in deltas
    }


def first_safe_index(staircase: dict[int, int], threshold: int, lo: int, hi: int) -> int:
    for delta in range(lo, hi + 1):
        if staircase[delta] <= threshold:
            return delta
    raise AssertionError("bracket does not contain a safe index")


def toy_check() -> dict[str, object]:
    lists_by_word = {
        "U0": {
            3: {"c0", "c1", "c2", "c3", "c4"},
            4: {"c0", "c1", "c2"},
            5: {"c0"},
            6: set(),
        },
        "U1": {
            3: {"d0", "d1", "d2", "d3"},
            4: {"d0", "d1"},
            5: {"d0", "d1"},
            6: {"d0"},
        },
    }
    threshold = 2
    lo = 4
    hi = 6
    staircase = supremum_staircase(lists_by_word)
    first_safe = first_safe_index(staircase, threshold, lo, hi)
    values = [staircase[delta] for delta in sorted(staircase)]
    return {
        "nested_by_received_word": nested_by_delta(lists_by_word),
        "supremum_staircase": {str(key): value for key, value in staircase.items()},
        "integer_valued": all(isinstance(value, int) for value in staircase.values()),
        "nonincreasing": all(left >= right for left, right in zip(values, values[1:])),
        "threshold": threshold,
        "bracket": {
            "delta_lo": lo,
            "delta_hi": hi,
            "unsafe_at_lo": staircase[lo] > threshold,
            "safe_at_hi": staircase[hi] <= threshold,
        },
        "first_safe": first_safe,
        "adjacent_crossing_holds": staircase[first_safe - 1] > threshold
        and threshold >= staircase[first_safe],
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "list-crossing-localization-v1",
        "status": "PROVED",
        "source_dag_node": "list_crossing_localization",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove the pointwise list upper certificate",
            "does not prove the unsafe lower certificate",
            "does not prove a deployed row theorem",
        ],
        "note": "experimental/notes/thresholds/list_crossing_localization.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "list-crossing-localization-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    for key in ["nested_by_received_word", "integer_valued", "nonincreasing"]:
        if not toy.get(key):
            raise AssertionError(f"failed toy check: {key}")
    bracket = toy["bracket"]
    if not isinstance(bracket, dict) or not (
        bracket.get("unsafe_at_lo") and bracket.get("safe_at_hi")
    ):
        raise AssertionError("bracket check failed")
    if not toy.get("adjacent_crossing_holds"):
        raise AssertionError("adjacent crossing check failed")


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
