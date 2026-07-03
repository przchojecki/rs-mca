#!/usr/bin/env python3
"""Verify the E13 split-locator syzygy circuit lemma against stored records."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE = Path(
    "experimental/data/certificates/spread-regime-design-evidence/"
    "e13_sparse_greedy_syzygy_branch.json"
)
OUTPUT = Path(
    "experimental/data/certificates/spread-regime-design-evidence/"
    "e13_split_locator_syzygy_circuit_lemma.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_records(source: dict[str, Any]):
    for cell in source["cells"]:
        for record in cell["exception_records"]:
            yield cell, record


def block_weight(record: dict[str, Any]) -> int:
    return sum(
        1
        for block in record["relation_coefficients_by_block"]
        if any(int(coeff) for coeff in block)
    )


def check_record(cell: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    block_count = len(record["family"])
    if record["relation_left_nullity"] != 1:
        raise AssertionError(("left_nullity", cell["case_name"], record["subset_indices"]))
    if block_weight(record) != block_count:
        raise AssertionError(("support", cell["case_name"], record["subset_indices"]))
    if not record["relation_full_locator_support"]:
        raise AssertionError(("support flag", cell["case_name"], record["subset_indices"]))
    if not record["single_deletion_independence"]:
        raise AssertionError(("deletion flag", cell["case_name"], record["subset_indices"]))
    bad_deletions = [
        item for item in record["single_deletion_rank_records"]
        if item["degree_deficiency"] != 0
    ]
    if bad_deletions:
        raise AssertionError(("bad deletion", cell["case_name"], record["subset_indices"], bad_deletions))
    return {
        "case_name": cell["case_name"],
        "slope_mode": cell["slope_mode"],
        "size": cell["size"],
        "subset_indices": record["subset_indices"],
        "relation_left_nullity": record["relation_left_nullity"],
        "block_count": block_count,
        "nonzero_block_count": block_weight(record),
        "deletion_count": len(record["single_deletion_rank_records"]),
        "all_one_block_deletions_independent": True,
    }


def build_certificate() -> dict[str, Any]:
    source = json.loads(SOURCE.read_text())
    rows = []
    cell_counts: Counter[str] = Counter()
    deletion_count = 0
    for cell, record in iter_records(source):
        row = check_record(cell, record)
        rows.append(row)
        cell_counts[f"{cell['case_name']}::{cell['slope_mode']}::size{cell['size']}"] += 1
        deletion_count += row["deletion_count"]

    if len(rows) != source["total_nondegenerate_syzygy_exceptions"]:
        raise AssertionError((len(rows), source["total_nondegenerate_syzygy_exceptions"]))
    if not source["all_exceptions_have_one_dimensional_left_nullspace"]:
        raise AssertionError("source left-nullity flag is false")
    if not source["all_relations_have_full_locator_support"]:
        raise AssertionError("source full-support flag is false")
    if not source["all_single_deletions_are_independent"]:
        raise AssertionError("source deletion-independence flag is false")

    return {
        "schema": "e13-split-locator-syzygy-circuit-lemma-v1",
        "status": "PASS",
        "source_artifact": str(SOURCE),
        "source_sha256": sha256_file(SOURCE),
        "dag_nodes": ["spread_exception_classification", "spread_regime_bound"],
        "lemma": (
            "Left dependencies among split-locator rows are equivalent to the "
            "two displayed zero-polynomial identities.  One-dimensional "
            "full-support dependencies whose one-block deletions are "
            "independent are minimal circuits."
        ),
        "records_checked": len(rows),
        "cell_counts": dict(sorted(cell_counts.items())),
        "total_one_block_deletions_checked": deletion_count,
        "all_records_are_minimal_full_support_circuits": True,
        "sample_records": rows[:8],
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def print_summary(certificate: dict[str, Any]) -> None:
    print("E13 split-locator syzygy circuit lemma")
    print(f"  status: {certificate['status']}")
    print(f"  records checked: {certificate['records_checked']}")
    print(f"  one-block deletions checked: {certificate['total_one_block_deletions_checked']}")
    for cell, count in certificate["cell_counts"].items():
        print(f"  {cell}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    print_summary(certificate)
    if args.check:
        stored = json.loads(args.check.read_text())
        if stored != certificate:
            raise AssertionError(f"certificate mismatch: {args.check}")
        print(f"checked {args.check}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if certificate["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
