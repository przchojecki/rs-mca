#!/usr/bin/env python3
"""Verify the M5 first-match stratification partition theorem.

The theorem is combinatorial.  Given ordered predicates T0..T6 and a final
catch-all residual predicate T7, the first matching leaf partitions every finite
candidate set.  This verifier checks the leaf implementation, allowed labels,
and seeded root-set dedup examples used by the proof note.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


OUTPUT = Path(
    "experimental/data/certificates/m5-stratification-partition/"
    "m5_stratification_partition_certificate.json"
)
FIELD_MODULUS = 97
RANDOM_SEED = 2026070208
RANDOM_TRIALS = 500

BOOL_FLAGS = (
    "contained_pair",
    "degenerate_pair",
    "tangent_paid",
    "quotient_paid",
    "extension_paid",
    "higher_agreement_dedup",
    "closed_chart",
)

VALID_CLOSED_STATUSES = {"eliminant", "empty", "dimension_degree"}
VALID_RESIDUAL_LABELS = {
    "quotient",
    "tangent",
    "extension",
    "candidate_new_obstruction",
    "unknown",
}


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class Leaf:
    leaf_id: str
    terminal_label: str
    predicate: Callable[[dict], bool]


def has_closed_status(record: dict) -> bool:
    return record.get("chart_status") in VALID_CLOSED_STATUSES


LEAVES = (
    Leaf("T0", "excluded", lambda row: bool(row.get("contained_pair"))),
    Leaf("T1", "paid:degenerate", lambda row: bool(row.get("degenerate_pair"))),
    Leaf("T2", "paid:tangent", lambda row: bool(row.get("tangent_paid"))),
    Leaf("T3", "paid:quotient", lambda row: bool(row.get("quotient_paid"))),
    Leaf("T4", "paid:extension", lambda row: bool(row.get("extension_paid"))),
    Leaf(
        "T5",
        "dedup:higher_agreement",
        lambda row: bool(row.get("higher_agreement_dedup")),
    ),
    Leaf("T6", "closed_chart", has_closed_status),
)


def classify(record: dict) -> dict:
    chart_status = record.get("chart_status")
    if chart_status is not None and chart_status not in VALID_CLOSED_STATUSES:
        raise ValueError(f"bad chart_status: {chart_status}")
    residual_label = record.get("residual_label", "unknown")
    if residual_label not in VALID_RESIDUAL_LABELS:
        raise ValueError(f"bad residual_label: {residual_label}")

    for leaf in LEAVES:
        if leaf.predicate(record):
            label = chart_status if leaf.leaf_id == "T6" else leaf.terminal_label
            return {
                "leaf_id": leaf.leaf_id,
                "terminal_label": label,
                "residual_label": None,
            }
    return {
        "leaf_id": "T7",
        "terminal_label": f"residual:{residual_label}",
        "residual_label": residual_label,
    }


def bool_record(mask: int) -> dict:
    record = {}
    for index, flag in enumerate(BOOL_FLAGS):
        record[flag] = bool(mask & (1 << index))
    if record["closed_chart"]:
        record["chart_status"] = "eliminant"
    else:
        record["chart_status"] = None
    record["residual_label"] = "unknown"
    return record


def exhaustive_overlap_check() -> dict:
    outcomes = []
    counts: dict[str, int] = {}
    for mask in range(1 << len(BOOL_FLAGS)):
        record = bool_record(mask)
        result = classify(record)
        counts[result["leaf_id"]] = counts.get(result["leaf_id"], 0) + 1
        outcomes.append({
            "mask": mask,
            "true_flags": [flag for i, flag in enumerate(BOOL_FLAGS) if mask & (1 << i)],
            "leaf_id": result["leaf_id"],
            "terminal_label": result["terminal_label"],
        })
    if sum(counts.values()) != 1 << len(BOOL_FLAGS):
        raise AssertionError("exhaustive masks not total")
    return {
        "non_residual_predicates": len(BOOL_FLAGS),
        "masks_checked": 1 << len(BOOL_FLAGS),
        "leaf_counts": counts,
        "outcome_hash": sha256_json(outcomes),
    }


def invalid_label_checks() -> dict:
    rejected = []
    for bad in ("root_table", "closed", "mystery"):
        try:
            classify({"chart_status": bad})
        except ValueError:
            rejected.append({"field": "chart_status", "value": bad})
        else:
            raise AssertionError(("accepted bad chart_status", bad))
    for bad in ("periodic", "paid", "new"):
        try:
            classify({"residual_label": bad})
        except ValueError:
            rejected.append({"field": "residual_label", "value": bad})
        else:
            raise AssertionError(("accepted bad residual_label", bad))
    return {"rejected_count": len(rejected), "rejected": rejected}


def random_root_record(rng: random.Random) -> dict:
    record = {flag: bool(rng.getrandbits(1)) for flag in BOOL_FLAGS[:-1]}
    status_roll = rng.randrange(5)
    if status_roll < 3:
        record["chart_status"] = sorted(VALID_CLOSED_STATUSES)[status_roll]
        record["closed_chart"] = True
    else:
        record["chart_status"] = None
        record["closed_chart"] = False
    record["residual_label"] = rng.choice(sorted(VALID_RESIDUAL_LABELS))
    return record


def partition_root_sets(records: dict[int, dict]) -> dict[str, list[int]]:
    leaves: dict[str, list[int]] = {}
    for root, record in records.items():
        result = classify(record)
        label = result["terminal_label"]
        leaves.setdefault(label, []).append(root)
    for roots in leaves.values():
        roots.sort()
    return dict(sorted(leaves.items()))


def random_partition_checks() -> dict:
    rng = random.Random(RANDOM_SEED)
    fingerprints = []
    terminal_labels = set()
    for _ in range(RANDOM_TRIALS):
        size = rng.randint(1, FIELD_MODULUS)
        roots = rng.sample(range(FIELD_MODULUS), size)
        records = {root: random_root_record(rng) for root in roots}
        leaves = partition_root_sets(records)
        flattened = sorted(root for values in leaves.values() for root in values)
        if flattened != sorted(roots):
            raise AssertionError("partition not total")
        if len(flattened) != len(set(flattened)):
            raise AssertionError("partition double-counted a root")
        terminal_labels.update(leaves)
        fingerprints.append(sha256_json(leaves))
    return {
        "field_modulus": FIELD_MODULUS,
        "seed": RANDOM_SEED,
        "trials": RANDOM_TRIALS,
        "terminal_labels_seen": sorted(terminal_labels),
        "fingerprint_hash": sha256_json(fingerprints),
    }


def mixed_overlap_example() -> dict:
    records = {
        3: {"tangent_paid": True, "quotient_paid": True, "residual_label": "unknown"},
        5: {"quotient_paid": True, "extension_paid": True, "residual_label": "unknown"},
        8: {"extension_paid": True, "chart_status": "eliminant"},
        13: {"higher_agreement_dedup": True, "chart_status": "eliminant"},
        21: {"chart_status": "eliminant"},
        34: {"chart_status": "empty"},
        55: {"chart_status": "dimension_degree"},
        89: {"residual_label": "candidate_new_obstruction"},
    }
    leaves = partition_root_sets(records)
    naive_claim_count = 0
    for record in records.values():
        naive_claim_count += int(bool(record.get("tangent_paid")))
        naive_claim_count += int(bool(record.get("quotient_paid")))
        naive_claim_count += int(bool(record.get("extension_paid")))
        naive_claim_count += int(bool(record.get("higher_agreement_dedup")))
        naive_claim_count += int(record.get("chart_status") in VALID_CLOSED_STATUSES)
        naive_claim_count += 1
    first_match_count = sum(len(values) for values in leaves.values())
    if first_match_count != len(records):
        raise AssertionError("mixed example not total")
    if naive_claim_count <= first_match_count:
        raise AssertionError("mixed example failed to exhibit overlap pressure")
    return {
        "root_count": len(records),
        "naive_claim_count": naive_claim_count,
        "first_match_count": first_match_count,
        "leaves": leaves,
    }


def build_certificate() -> dict:
    source = Path(__file__).read_text(encoding="utf-8")
    return {
        "schema": "m5-stratification-partition-v1",
        "status": "PROVED_COMBINATORIAL_WITH_FINITE_REPLAY",
        "dag_node": "stratification_partition_thm",
        "queue_item": "Q2.10",
        "ordered_leaves": [
            {
                "leaf_id": leaf.leaf_id,
                "terminal_label": leaf.terminal_label,
            }
            for leaf in LEAVES
        ] + [{
            "leaf_id": "T7",
            "terminal_label": "residual:<label>",
        }],
        "valid_closed_statuses": sorted(VALID_CLOSED_STATUSES),
        "valid_residual_labels": sorted(VALID_RESIDUAL_LABELS),
        "exhaustive_overlap_check": exhaustive_overlap_check(),
        "invalid_label_checks": invalid_label_checks(),
        "random_partition_checks": random_partition_checks(),
        "mixed_overlap_example": mixed_overlap_example(),
        "script_sha256": hashlib.sha256(source.encode()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    certificate = build_certificate()
    print("=" * 78)
    print("M5 stratification partition theorem")
    print("=" * 78)
    print(f"classification: {certificate['status']}")
    print(
        "exhaustive masks checked:",
        certificate["exhaustive_overlap_check"]["masks_checked"],
    )
    print(
        "random root-set partitions:",
        certificate["random_partition_checks"]["trials"],
    )
    print(
        "mixed example naive/first-match:",
        certificate["mixed_overlap_example"]["naive_claim_count"],
        "/",
        certificate["mixed_overlap_example"]["first_match_count"],
    )
    print("[PASS] first-match leaves are total and disjoint")
    if args.emit:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
