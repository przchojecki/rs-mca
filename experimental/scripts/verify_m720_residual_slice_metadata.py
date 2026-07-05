#!/usr/bin/env python3
"""Replay the M720 residual slice-metadata classifier."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


COUNT_CEILING = 6_000_000
REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m720" / "m720_residual_slice_metadata.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m720-residual-slice-metadata"
    / "m720_residual_slice_metadata.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "m720_residual_slice_metadata",
    "window_rule": "C(W-1,h-1) + C(W,h) <= 6,000,000",
    "over_ceiling": "n=32, h=16, q_exp=2",
    "non_claim": "does not promote `W<n`",
}


def chosen_window(n: int, h: int) -> tuple[int, int]:
    best = 2 * h
    best_cost = comb(best - 1, h - 1) + comb(best, h)
    w = 2 * h
    while w <= n:
        cost = comb(w - 1, h - 1) + comb(w, h)
        if cost <= COUNT_CEILING:
            best = w
            best_cost = cost
            w += 1
        else:
            break
    return best, best_cost


def classify_cells() -> dict[str, Any]:
    under_ceiling_complete = []
    over_ceiling_complete = []
    slices = []
    for h in range(7, 21):
        for n in (16, 32, 64, 128, 256, 1024):
            if n < 2 * h:
                continue
            w, cost = chosen_window(n, h)
            for q_exp in (2, 3):
                rec = {
                    "n": n,
                    "h": h,
                    "q_exp": q_exp,
                    "W": w,
                    "cost": cost,
                }
                if w == n and cost <= COUNT_CEILING:
                    under_ceiling_complete.append(rec)
                elif w == n:
                    over_ceiling_complete.append(rec)
                else:
                    slices.append(rec)
    return {
        "under_ceiling_complete": under_ceiling_complete,
        "over_ceiling_complete": over_ceiling_complete,
        "window_slices": slices,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    classification = classify_cells()
    cert = {
        "schema": "m720-residual-slice-metadata-v1",
        "status": "PROVED_RESIDUAL_SLICE_METADATA_REPLAY",
        "source_dag_node": "m720_residual_slice_metadata",
        "count_ceiling": COUNT_CEILING,
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "classification": classification,
        "expected_under_ceiling_complete": [
            {"n": 16, "h": 7, "q_exp": 2},
            {"n": 16, "h": 7, "q_exp": 3},
            {"n": 32, "h": 7, "q_exp": 2},
            {"n": 32, "h": 7, "q_exp": 3},
            {"n": 16, "h": 8, "q_exp": 2},
            {"n": 16, "h": 8, "q_exp": 3},
        ],
        "expected_over_ceiling_complete": [
            {"n": 32, "h": 16, "q_exp": 2},
            {"n": 32, "h": 16, "q_exp": 3},
        ],
        "non_claims": [
            "does not prove zero unpaid non-toral survivors",
            "does not promote W<n window slices to complete certificates",
        ],
        "note": "experimental/notes/m720/m720_residual_slice_metadata.md",
    }
    validate(cert)
    return cert


def triples(records: list[dict[str, int]]) -> set[tuple[int, int, int]]:
    return {(record["n"], record["h"], record["q_exp"]) for record in records}


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "m720-residual-slice-metadata-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")

    classification = cert["classification"]
    expected_under = triples(cert["expected_under_ceiling_complete"])
    expected_over = triples(cert["expected_over_ceiling_complete"])
    got_under = triples(classification["under_ceiling_complete"])
    got_over = triples(classification["over_ceiling_complete"])
    if got_under != expected_under:
        raise AssertionError(f"under-ceiling complete mismatch: {got_under}")
    if got_over != expected_over:
        raise AssertionError(f"over-ceiling complete mismatch: {got_over}")
    bad_slices = [row for row in classification["window_slices"] if row["W"] >= row["n"]]
    if bad_slices:
        raise AssertionError(f"slice rows not proper slices: {bad_slices}")


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
        c = cert["classification"]
        print(
            f"{cert['status']}: "
            f"under={len(c['under_ceiling_complete'])}, "
            f"over={len(c['over_ceiling_complete'])}, "
            f"slices={len(c['window_slices'])}"
        )


if __name__ == "__main__":
    main()
