#!/usr/bin/env python3
"""Replay the E22 minimal-scale partition packet."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "e22_minimal_scale_partition.md"
SELECTOR_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e22-dyadic-minimal-scale-selector"
    / "e22_dyadic_minimal_scale_selector.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e22-minimal-scale-partition"
    / "e22_minimal_scale_partition.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e22_minimal_scale_partition",
    "dependency": "e22_dyadic_minimal_scale_selector",
    "predicate": "|B_M(R)| < M",
    "partition": "disjoint and exhaustive partition",
    "non_claim": "does not evaluate a pricing column",
}


def nonempty_subsets(items: list[int]):
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def dependency_check() -> dict[str, object]:
    cert = json.loads(SELECTOR_CERT.read_text(encoding="utf-8"))
    return {
        "path": str(SELECTOR_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("schema") == "e22-dyadic-minimal-scale-selector-v1"
        and cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "e22_dyadic_minimal_scale_selector",
    }


def partition_check() -> dict[str, object]:
    summaries = []
    for exponent in range(2, 10):
        moduli = [2**i for i in range(1, exponent + 1)]
        cells = {modulus: [] for modulus in moduli}
        for admissible_tuple in nonempty_subsets(moduli):
            admissible = set(admissible_tuple)
            minimal = min(admissible)
            tail_minimal_cells = [
                modulus
                for modulus in moduli
                if modulus in admissible
                and all(smaller not in admissible for smaller in moduli if smaller < modulus)
            ]
            if tail_minimal_cells != [minimal]:
                raise AssertionError((moduli, admissible, tail_minimal_cells))
            cells[minimal].append(frozenset(admissible))

        seen = set()
        for members in cells.values():
            for member in members:
                if member in seen:
                    raise AssertionError("partition cell overlap")
                seen.add(member)
        expected = 2 ** len(moduli) - 1
        if len(seen) != expected:
            raise AssertionError("partition is not exhaustive")
        summaries.append(
            {
                "chain_length": len(moduli),
                "moduli": moduli,
                "nonempty_admissible_sets": expected,
                "covered_sets": len(seen),
                "occupied_cells": sum(1 for members in cells.values() if members),
            }
        )
    return {"checked_chain_lengths": [row["chain_length"] for row in summaries], "summaries": summaries, "all_checks_pass": True}


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "e22-minimal-scale-partition-v1",
        "status": "PROVED",
        "source_dag_node": "e22_minimal_scale_partition",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "partition_check": partition_check(),
        "non_claims": [
            "does not compute cross-scale overlap counts",
            "does not evaluate a pricing column",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/e22_minimal_scale_partition.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "e22-minimal-scale-partition-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "e22_minimal_scale_partition":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    check = cert.get("partition_check")
    if not isinstance(check, dict) or not check.get("all_checks_pass"):
        raise AssertionError("partition check failed")


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
