#!/usr/bin/env python3
"""Verify the compact Cycle84 projected-census receipt.

This nonmutating verifier checks the recorded output of the heavy tau-folded
projected duplicate-bin census against the current lightweight certificates.
It verifies receipt arithmetic and consistency with:

* the projected-log certificate;
* the color-shell count;
* the 30 kernel-lift candidates.

It does not rerun the heavy projected census. Its job is to make the imported
finite computation reviewer-facing and mechanically tied to the current M1
fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_RECEIPT = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "witnesses"
    / "m1-cycle84"
    / "projected_census_receipt.json"
)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_color_collision_witnesses as color_witness
import verify_m1_cycle84_kernel_lift_candidates as kernel_lift
import verify_m1_cycle84_projected_log_certificate as log_cert


EXPECTED_SOURCE_COMMIT = "fdb3cac"
EXPECTED_SOURCE_PATH = (
    "experimental/certificates/cycle84_finite_certificate/output/tau_opt.out"
)
EXPECTED_SOURCE_SHA256 = (
    "65bc5cf766497c9b31a1c71856a129023d72a314ab392ddf5509a72b40e96849"
)
EXPECTED_DECISION = "TAU_FOLDED_PROJECTED_MMAX_LE_12"
EXPECTED_SHARDS = 16_384
EXPECTED_THREADS = 16
EXPECTED_DUPLICATE_BINS = 30
EXPECTED_DUPLICATE_COUNT = 2


def load_json(path: Path) -> tuple[bytes, Dict[str, Any]]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def projected_keys_from_kernel() -> list[int]:
    return [int(candidate[0]) for candidate in kernel_lift.PROJECTED_LIFT_CANDIDATES]


def duplicate_keys(bins: Sequence[Dict[str, Any]]) -> list[int]:
    return [int(item["key"]) for item in bins]


def duplicate_counts(bins: Sequence[Dict[str, Any]]) -> list[int]:
    return [int(item["count"]) for item in bins]


def duplicate_shards(bins: Sequence[Dict[str, Any]]) -> list[int]:
    return [int(item["shard"]) for item in bins]


def ordered_energy_from_counts(counts: Sequence[int]) -> int:
    return sum(count * (count - 1) for count in counts)


def assert_all(checks: Dict[str, bool]) -> None:
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")


def build_report(receipt_path: Path = DEFAULT_RECEIPT) -> Dict[str, Any]:
    raw, receipt = load_json(receipt_path)
    log_report = log_cert.build_report()
    color_report = color_witness.build_report()
    kernel_report = kernel_lift.build_report()

    bins = receipt["duplicate_canonical_bins"]
    keys = duplicate_keys(bins)
    counts = duplicate_counts(bins)
    shards = duplicate_shards(bins)
    kernel_keys = projected_keys_from_kernel()
    folded_energy = ordered_energy_from_counts(counts)
    color_shell_size = int(color_report["color_shell"]["compatible_tuple_count"])
    fixed_counts = [int(value) for value in receipt["fixed_selected_counts"]]

    checks = {
        "source_commit_recorded": (
            receipt["source"]["commit"] == EXPECTED_SOURCE_COMMIT
        ),
        "source_path_recorded": receipt["source"]["path"] == EXPECTED_SOURCE_PATH,
        "source_sha256_recorded": (
            receipt["source"]["sha256"] == EXPECTED_SOURCE_SHA256
        ),
        "decision_matches": receipt["decision"] == EXPECTED_DECISION,
        "projection_modulus_matches_log_certificate": (
            int(receipt["projection_modulus"]) == log_cert.M
            == int(log_report["model"]["M"])
        ),
        "kernel_order_matches": int(receipt["kernel_order"]) == log_cert.N // log_cert.M,
        "kappa_matches_log_certificate": (
            int(receipt["kappa"]) == int(log_report["tau_projection"]["kappa"])
        ),
        "fixed_roots_match_log_certificate": (
            [int(value) for value in receipt["fixed_roots"]]
            == [int(value) for value in log_report["tau_projection"]["fixed_roots"]]
        ),
        "fixed_roots_have_zero_selected_counts": fixed_counts == [0, 0],
        "tau_half_domain_counted_matches_expected": (
            int(receipt["tau_half_domain_counted"])
            == int(receipt["tau_half_domain_expected"])
        ),
        "tau_half_domain_matches_color_shell": (
            2 * int(receipt["tau_half_domain_expected"]) == color_shell_size
        ),
        "canonical_shards_match": int(receipt["canonical_shards"]) == EXPECTED_SHARDS,
        "threads_match_recorded_run": int(receipt["threads"]) == EXPECTED_THREADS,
        "duplicate_bin_count_matches": len(bins) == EXPECTED_DUPLICATE_BINS,
        "duplicate_keys_strictly_increasing": keys == sorted(keys),
        "duplicate_keys_distinct": len(set(keys)) == len(keys),
        "duplicate_counts_all_two": all(count == EXPECTED_DUPLICATE_COUNT for count in counts),
        "duplicate_shards_in_range": all(
            0 <= shard < int(receipt["canonical_shards"]) for shard in shards
        ),
        "duplicate_keys_match_kernel_lift_candidates": keys == kernel_keys,
        "folded_energy_matches_duplicate_counts": (
            int(receipt["folded_ordered_energy"]) == folded_energy
        ),
        "projected_energy_twice_folded": (
            int(receipt["projected_ordered_energy"]) == 2 * folded_energy
        ),
        "max_canonical_multiplicity_matches_counts": (
            int(receipt["max_canonical_projected_multiplicity"]) == max(counts)
        ),
        "full_projected_max_including_fixed_matches": (
            int(receipt["full_projected_max_including_fixed"])
            == max(max(counts), *(fixed_counts or [0]))
        ),
        "projected_log_certificate_passes": log_report["status"] == "PASS",
        "color_shell_verifier_passes": color_report["status"] == "PASS",
        "kernel_lift_verifier_passes": kernel_report["status"] == "PASS",
        "kernel_lift_checks_same_30_bins": (
            int(kernel_report["projected_lift"]["projected_duplicate_bins_checked"])
            == len(bins)
        ),
    }
    assert_all(checks)

    return {
        "status": "PASS",
        "proof_status": (
            "AUDIT / FINITE-MODEL-PROJECTED-CENSUS-RECEIPT-VERIFIED / "
            "CONDITIONAL"
        ),
        "theorem_problem_id": "M1 Cycle84 projected census receipt",
        "receipt_path": str(receipt_path.relative_to(REPO_ROOT)),
        "receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "source": receipt["source"],
        "census": {
            "decision": receipt["decision"],
            "projection_modulus": int(receipt["projection_modulus"]),
            "kernel_order": int(receipt["kernel_order"]),
            "tau_half_domain_counted": int(receipt["tau_half_domain_counted"]),
            "color_shell_size": color_shell_size,
            "duplicate_canonical_bins": len(bins),
            "duplicate_count_per_bin": EXPECTED_DUPLICATE_COUNT,
            "folded_ordered_energy": folded_energy,
            "projected_ordered_energy": int(receipt["projected_ordered_energy"]),
            "max_canonical_projected_multiplicity": int(
                receipt["max_canonical_projected_multiplicity"]
            ),
            "full_projected_max_including_fixed": int(
                receipt["full_projected_max_including_fixed"]
            ),
        },
        "duplicate_keys": keys,
        "checks": checks,
        "remaining_import": (
            "independent replay or source-code audit of the heavy tau-folded "
            "projected duplicate-bin census that produced this receipt"
        ),
        "imports_required": [
            "heavy projected tau-folded census replay/generator correctness",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    census = report["census"]

    print("m1_cycle84_projected_census_receipt: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"receipt={report['receipt_path']}")
    print(f"receipt_sha256={report['receipt_sha256']}")
    print(
        "census="
        f"decision={census['decision']}, "
        f"half_domain={census['tau_half_domain_counted']}, "
        f"color_shell={census['color_shell_size']}, "
        f"duplicate_bins={census['duplicate_canonical_bins']}, "
        f"max={census['full_projected_max_including_fixed']}"
    )
    print(
        "energy="
        f"folded={census['folded_ordered_energy']}, "
        f"projected={census['projected_ordered_energy']}"
    )
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle84 projected-census receipt."
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=DEFAULT_RECEIPT,
        help="path to the projected census receipt JSON",
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
