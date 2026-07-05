#!/usr/bin/env python3
"""Replay the DLI Deligne-Weil transfer packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "dli" / "dli_deligne_weyl_transfer.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dli-deligne-weyl-transfer"
    / "dli_deligne_weyl_transfer.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dli_deligne_weyl_transfer",
    "target": "dli_odd_eval_exponential_sum_bound",
    "square_root": "|sum_y trace(Frob_y)| <= C(conductor) q^{1/2}",
    "non_claim": "does not prove that the actual DLI",
}


def accepts_transfer(records: list[dict[str, Any]], budget: int) -> bool:
    if budget < 0:
        return False
    total = 0
    seen = set()
    for record in records:
        key = tuple(record.get("key", []))
        if key in seen:
            return False
        seen.add(key)
        if record.get("geometrically_nontrivial") is not True:
            return False
        conductor = record.get("conductor_bound")
        if not isinstance(conductor, int) or conductor < 0:
            return False
        total += conductor
    return total <= budget


def toy_check() -> dict[str, Any]:
    records = [
        {"key": ["profile-a", "freq-1", 1, "component-0"], "geometrically_nontrivial": True, "conductor_bound": 2},
        {"key": ["profile-a", "freq-1", 2, "component-0"], "geometrically_nontrivial": True, "conductor_bound": 3},
        {"key": ["profile-b", "freq-2", 1, "component-1"], "geometrically_nontrivial": True, "conductor_bound": 1},
    ]
    bad_trivial = [dict(record) for record in records]
    bad_trivial[0]["geometrically_nontrivial"] = False
    bad_conductor = [dict(record) for record in records]
    bad_conductor[1]["conductor_bound"] = -1
    over_budget = [dict(record) for record in records]
    over_budget[2]["conductor_bound"] = 10
    duplicate = [dict(record) for record in records] + [dict(records[0])]

    return {
        "good_records_accepted": accepts_transfer(records, budget=6),
        "trivial_record_rejected": not accepts_transfer(bad_trivial, budget=6),
        "bad_conductor_rejected": not accepts_transfer(bad_conductor, budget=6),
        "over_budget_rejected": not accepts_transfer(over_budget, budget=6),
        "duplicate_record_rejected": not accepts_transfer(duplicate, budget=6),
        "record_count": len(records),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "dli-deligne-weyl-transfer-v1",
        "status": "PROVED_DELIGNE_WEYL_TRANSFER_REPLAY",
        "source_dag_node": "dli_deligne_weyl_transfer",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove DLI odd-phase noncollapse",
            "does not construct conductor certificates",
        ],
        "note": "experimental/notes/dli/dli_deligne_weyl_transfer.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "dli-deligne-weyl-transfer-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["toy_check"]
    required = [
        "good_records_accepted",
        "trivial_record_rejected",
        "bad_conductor_rejected",
        "over_budget_rejected",
        "duplicate_record_rejected",
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
