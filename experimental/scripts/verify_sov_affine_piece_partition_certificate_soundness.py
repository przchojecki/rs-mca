#!/usr/bin/env python3
"""Replay the SOV affine-piece partition certificate-soundness packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "sov" / "sov_affine_piece_partition_certificate_soundness.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "sov-affine-piece-partition-certificate-soundness"
    / "sov_affine_piece_partition_certificate_soundness.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "sov_affine_piece_partition_certificate_soundness",
    "target": "sov_hminus1_affine_piece_decomposition",
    "cancellation_dependency": "sov_nonconstant_affine_character_cancellation",
    "non_claim": "does not construct",
}

ALLOWED_EXCEPTIONAL_KINDS = {"paid", "norm_structured"}


def accepts_partition(certificate: dict[str, Any]) -> bool:
    universe = set(certificate["universe"])
    affine = certificate["affine_pieces"]
    exceptional = certificate["exceptional_pieces"]
    budget = certificate["exceptional_budget"]

    pieces = [set(piece["points"]) for piece in affine] + [set(piece["points"]) for piece in exceptional]
    covered = set().union(*pieces) if pieces else set()
    if covered != universe:
        return False

    seen: set[str] = set()
    for piece in pieces:
        if not seen.isdisjoint(piece):
            return False
        seen |= piece

    for piece in affine:
        if piece.get("coefficient_map") != "[X^{h-1}]L":
            return False
        if piece.get("linear_part_nonzero") is not True:
            return False

    for piece in exceptional:
        if piece.get("kind") not in ALLOWED_EXCEPTIONAL_KINDS:
            return False

    return sum(len(piece["points"]) for piece in exceptional) < budget


def toy_certificate() -> dict[str, Any]:
    return {
        "universe": ["L0", "L1", "L2", "L3", "L4"],
        "affine_pieces": [
            {"name": "P0", "points": ["L0", "L1"], "coefficient_map": "[X^{h-1}]L", "linear_part_nonzero": True},
            {"name": "P1", "points": ["L2", "L3"], "coefficient_map": "[X^{h-1}]L", "linear_part_nonzero": True},
        ],
        "exceptional_pieces": [
            {"name": "E0", "points": ["L4"], "kind": "paid"},
        ],
        "exceptional_budget": 2,
    }


def toy_check() -> dict[str, Any]:
    good = toy_certificate()
    missing = json.loads(json.dumps(good))
    missing["affine_pieces"][1]["points"] = ["L2"]
    overlap = json.loads(json.dumps(good))
    overlap["exceptional_pieces"][0]["points"] = ["L3", "L4"]
    constant_piece = json.loads(json.dumps(good))
    constant_piece["affine_pieces"][0]["linear_part_nonzero"] = False
    bad_exception = json.loads(json.dumps(good))
    bad_exception["exceptional_pieces"][0]["kind"] = "unpaid_unknown"
    too_large = json.loads(json.dumps(good))
    too_large["exceptional_budget"] = 1

    return {
        "good_certificate_accepted": accepts_partition(good),
        "missing_point_rejected": not accepts_partition(missing),
        "overlap_rejected": not accepts_partition(overlap),
        "constant_affine_piece_rejected": not accepts_partition(constant_piece),
        "bad_exceptional_kind_rejected": not accepts_partition(bad_exception),
        "over_budget_rejected": not accepts_partition(too_large),
        "universe_size": len(good["universe"]),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "sov-affine-piece-partition-certificate-soundness-v1",
        "status": "PROVED_PARTITION_CERTIFICATE_REPLAY",
        "source_dag_node": "sov_affine_piece_partition_certificate_soundness",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not construct the anchored-core partitions",
            "does not prove the conditional affine-piece decomposition payload by itself",
        ],
        "note": "experimental/notes/sov/sov_affine_piece_partition_certificate_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "sov-affine-piece-partition-certificate-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_certificate_accepted",
        "missing_point_rejected",
        "overlap_rejected",
        "constant_affine_piece_rejected",
        "bad_exceptional_kind_rejected",
        "over_budget_rejected",
    ]
    if not all(check[name] for name in required):
        raise AssertionError(f"failed toy check: {check}")


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
        print(f"{cert['status']}: {cert['toy_check']}")


if __name__ == "__main__":
    main()
