#!/usr/bin/env python3
"""Replay the E22 dyadic-chain Mobius accounting packet."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "e22_dyadic_chain_mobius_accounting.md"
PARTITION_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e22-minimal-scale-partition"
    / "e22_minimal_scale_partition.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e22-dyadic-chain-mobius-accounting"
    / "e22_dyadic_chain_mobius_accounting.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e22_dyadic_chain_mobius_accounting",
    "dependency": "e22_minimal_scale_partition",
    "identity": "A_j = N_j + sum_{i<j} O_{i,j}.",
    "recovery": "N_j = A_j - sum_{i<j} O_{i,j}.",
    "non_claim": "does not evaluate an E22 pricing",
}


def nonempty_subsets(items: list[int]):
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def dependency_check() -> dict[str, object]:
    cert = json.loads(PARTITION_CERT.read_text(encoding="utf-8"))
    return {
        "path": str(PARTITION_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("schema") == "e22-minimal-scale-partition-v1"
        and cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "e22_minimal_scale_partition",
    }


def triangular_check() -> dict[str, object]:
    summaries = []
    for length in range(1, 9):
        scales = list(range(length))
        classes = [set(subset) for subset in nonempty_subsets(scales)]
        minimal = {idx: min(admissible) for idx, admissible in enumerate(classes)}
        rows = []
        for j in scales:
            raw = sum(1 for admissible in classes if j in admissible)
            selected = sum(
                1
                for idx, admissible in enumerate(classes)
                if j in admissible and minimal[idx] == j
            )
            overlaps = sum(
                1
                for i in scales
                if i < j
                for idx, admissible in enumerate(classes)
                if j in admissible and minimal[idx] == i
            )
            if raw != selected + overlaps:
                raise AssertionError((length, j, raw, selected, overlaps))
            rows.append({"scale_index": j, "raw": raw, "selected": selected, "overlaps": overlaps})
        summaries.append({"chain_length": length, "class_count": len(classes), "rows": rows})
    return {
        "checked_chain_lengths": [row["chain_length"] for row in summaries],
        "summaries": summaries,
        "all_checks_pass": True,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "e22-dyadic-chain-mobius-accounting-v1",
        "status": "PROVED",
        "source_dag_node": "e22_dyadic_chain_mobius_accounting",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "triangular_check": triangular_check(),
        "non_claims": [
            "does not compute arithmetic overlap formulas",
            "does not evaluate an E22 pricing column",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/e22_dyadic_chain_mobius_accounting.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "e22-dyadic-chain-mobius-accounting-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "e22_dyadic_chain_mobius_accounting":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    check = cert.get("triangular_check")
    if not isinstance(check, dict) or not check.get("all_checks_pass"):
        raise AssertionError("triangular check failed")


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
