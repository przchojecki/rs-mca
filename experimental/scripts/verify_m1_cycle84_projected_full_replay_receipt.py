#!/usr/bin/env python3
"""Verify the saved Cycle84 all-shards projected-census replay receipt.

This nonmutating verifier checks the compact JSON receipt produced by

    python3 experimental/scripts/verify_m1_cycle84_projected_census_shard_replay.py \
        --all-shards --threads 16 --json

It does not rerun the 26.37-billion-entry projected census. It verifies that
the saved full-replay report matches the current archived census receipt and has
the all-shard equality checks enabled and passing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_FULL_REPLAY_RECEIPT = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "witnesses"
    / "m1-cycle84"
    / "projected_census_full_replay_receipt.json"
)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_projected_census_receipt as census_receipt
import verify_m1_cycle84_generated_replay_source as source_contract


EXPECTED_PROOF_STATUS = (
    "AUDIT / FINITE-MODEL-PROJECTED-CENSUS-FULL-REPLAYED / CONDITIONAL"
)
EXPECTED_THEOREM_ID = "M1 Cycle84 projected census shard replay"
REQUIRED_ALL_SHARD_CHECKS = [
    "all_shard_entries_match_receipt",
    "all_shard_energy_matches_receipt",
    "all_shard_max_matches_receipt",
]


def build_report(receipt_path: Path = DEFAULT_FULL_REPLAY_RECEIPT) -> Dict[str, Any]:
    raw = receipt_path.read_bytes()
    full = json.loads(raw)
    compact = census_receipt.build_report()
    source_report = source_contract.build_report()

    checks = {
        "saved_receipt_status_passes": full["status"] == "PASS",
        "proof_status_is_full_replay": full["proof_status"] == EXPECTED_PROOF_STATUS,
        "theorem_problem_id_matches": full["theorem_problem_id"] == EXPECTED_THEOREM_ID,
        "all_shards_flag_true": full["all_shards"] is True,
        "all_16384_shards_replayed": full["selected_shard_count"] == 16_384,
        "worker_count_recorded": int(full["threads"]) >= 1,
        "receipt_path_matches_compact_receipt": (
            full["receipt_path"] == compact["receipt_path"]
        ),
        "duplicate_bin_count_matches_compact_receipt": (
            full["duplicate_bins_replayed"]
            == compact["census"]["duplicate_canonical_bins"]
        ),
        "half_domain_count_matches_compact_receipt": (
            full["selected_entries"]
            == compact["census"]["tau_half_domain_counted"]
        ),
        "folded_energy_matches_compact_receipt": (
            full["selected_folded_ordered_energy"]
            == compact["census"]["folded_ordered_energy"]
        ),
        "max_multiplicity_matches_compact_receipt": (
            full["selected_max_canonical_projected_multiplicity"]
            == compact["census"]["max_canonical_projected_multiplicity"]
        ),
        "remaining_import_is_source_audit": (
            full["remaining_import"] == "source-code audit of this generated replay"
        ),
        "generated_source_contract_passes": source_report["status"] == "PASS",
        "generated_source_threads_match_receipt": (
            source_report["source"]["threads"] == full["threads"] == 16
        ),
        "all_embedded_checks_pass": all(full["checks"].values()),
        "all_shard_checks_present": all(
            name in full["checks"] for name in REQUIRED_ALL_SHARD_CHECKS
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FULL-REPLAY-RECEIPT-VERIFIED / CONDITIONAL",
        "theorem_problem_id": "M1 Cycle84 projected census full replay receipt",
        "receipt_path": str(receipt_path.relative_to(REPO_ROOT)),
        "receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "full_replay": {
            "selected_shard_count": full["selected_shard_count"],
            "threads": full["threads"],
            "selected_entries": full["selected_entries"],
            "duplicate_bins_replayed": full["duplicate_bins_replayed"],
            "folded_ordered_energy": full["selected_folded_ordered_energy"],
            "max_canonical_projected_multiplicity": (
                full["selected_max_canonical_projected_multiplicity"]
            ),
        },
        "generated_source": {
            "threads": source_report["source"]["threads"],
            "sha256": source_report["source"]["sha256"],
            "proof_status": source_report["proof_status"],
        },
        "checks": checks,
        "remaining_import": (
            "reviewer acceptance of the generated source contract for promotion "
            "beyond audit status"
        ),
        "imports_required": [
            "Cycle84 generated replay source contract",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    replay = report["full_replay"]
    source = report["generated_source"]
    print("m1_cycle84_projected_full_replay_receipt: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"receipt={report['receipt_path']}")
    print(f"receipt_sha256={report['receipt_sha256']}")
    print(
        "full_replay="
        f"shards={replay['selected_shard_count']}, "
        f"threads={replay['threads']}, "
        f"entries={replay['selected_entries']}, "
        f"duplicate_bins={replay['duplicate_bins_replayed']}, "
        f"energy={replay['folded_ordered_energy']}, "
        f"max={replay['max_canonical_projected_multiplicity']}"
    )
    print(f"generated_source=threads={source['threads']}, sha256={source['sha256']}")
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the saved Cycle84 all-shards replay receipt."
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=DEFAULT_FULL_REPLAY_RECEIPT,
        help="path to projected_census_full_replay_receipt.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()

    report = build_report(args.receipt)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
