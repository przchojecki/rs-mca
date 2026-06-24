#!/usr/bin/env python3
"""Verify the Cycle84 exact occupancy chain for the M1 finite model.

This nonmutating verifier composes the local Cycle84 checks:

* color shell and true collision witnesses;
* projected-log certificate;
* saved full projected-census replay receipt;
* generated C++ replay source contract;
* projected replay algorithm audit;
* kernel-lift filtering of all projected duplicate bins.

It concludes the exact finite-model occupancy
52,747,567,092, true ordered energy 24, and m_max=2, conditional on reviewer
acceptance of the generated source contract for promotion beyond audit status.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_color_collision_witnesses as color_witness
import verify_m1_cycle84_generated_replay_source as source_contract
import verify_m1_cycle84_kernel_lift_candidates as kernel_lift
import verify_m1_cycle84_projected_full_replay_receipt as full_replay
import verify_m1_cycle84_projected_log_certificate as log_cert
import verify_m1_cycle84_projected_replay_algorithm as replay_algorithm


EXPECTED_COLOR_SHELL_SIZE = 52_747_567_104
EXPECTED_OCCUPANCY = 52_747_567_092
EXPECTED_TRUE_DOUBLE_FIBERS = 12
EXPECTED_TRUE_ORDERED_ENERGY = 24
EXPECTED_M_MAX = 2
EXPECTED_PROJECTED_BINS = 30
EXPECTED_PROJECTED_WITNESSES = 60


def build_report() -> Dict[str, Any]:
    color_report = color_witness.build_report()
    log_report = log_cert.build_report()
    full_report = full_replay.build_report()
    source_report = source_contract.build_report()
    algorithm_report = replay_algorithm.build_report()
    kernel_report = kernel_lift.build_report()

    shell_size = int(color_report["color_shell"]["compatible_tuple_count"])
    full_replay_data = full_report["full_replay"]
    lift = kernel_report["projected_lift"]

    true_double_fibers = int(lift["true_double_fibers_after_tau"])
    true_energy = int(lift["true_ordered_energy_after_tau"])
    exact_occupancy = shell_size - true_double_fibers
    exact_m_max = int(full_replay_data["max_canonical_projected_multiplicity"])

    checks = {
        "color_shell_verifier_passes": color_report["status"] == "PASS",
        "projected_log_certificate_passes": log_report["status"] == "PASS",
        "full_projected_replay_receipt_passes": full_report["status"] == "PASS",
        "generated_replay_source_contract_passes": source_report["status"] == "PASS",
        "projected_replay_algorithm_audit_passes": (
            algorithm_report["status"] == "PASS"
        ),
        "kernel_lift_verifier_passes": kernel_report["status"] == "PASS",
        "color_shell_size_matches": shell_size == EXPECTED_COLOR_SHELL_SIZE,
        "full_replay_covers_all_shards": full_replay_data["selected_shard_count"] == 16_384,
        "full_replay_half_domain_is_half_shell": (
            2 * int(full_replay_data["selected_entries"]) == shell_size
        ),
        "projected_duplicate_bins_match": (
            int(full_replay_data["duplicate_bins_replayed"]) == EXPECTED_PROJECTED_BINS
            == int(lift["projected_duplicate_bins_checked"])
        ),
        "projected_witness_count_matches_bins": (
            int(lift["normalized_witnesses_checked"])
            == EXPECTED_PROJECTED_WITNESSES
            == 2 * int(full_replay_data["duplicate_bins_replayed"])
        ),
        "projected_max_multiplicity_two": (
            int(full_replay_data["max_canonical_projected_multiplicity"]) == 2
        ),
        "true_double_fibers_match": (
            true_double_fibers == EXPECTED_TRUE_DOUBLE_FIBERS
            == int(color_report["collision_witnesses"]["verified_double_fibers"])
        ),
        "true_ordered_energy_match": (
            true_energy == EXPECTED_TRUE_ORDERED_ENERGY
            == int(color_report["collision_witnesses"]["ordered_energy_contribution"])
        ),
        "exact_occupancy_matches": exact_occupancy == EXPECTED_OCCUPANCY,
        "exact_m_max_two": exact_m_max == EXPECTED_M_MAX,
        "no_fibers_of_size_at_least_3": exact_m_max < 3,
        "slot_table_digest_consistent": (
            color_report["slot_table_digest"]
            == kernel_report["slot_table_digest"]
            == log_report["slot_table_digest"]
        ),
        "algorithm_source_sha_matches_source_contract": (
            algorithm_report["generated_cycle84_source"]["sha256"]
            == source_report["source"]["sha256"]
            == full_report["generated_source"]["sha256"]
        ),
        "algorithm_source_contract_status_matches": (
            algorithm_report["generated_source_contract"]["proof_status"]
            == source_report["proof_status"]
        ),
        "full_replay_receipt_uses_generated_source_contract": (
            full_report["generated_source"]["proof_status"]
            == source_report["proof_status"]
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": (
            "AUDIT / FINITE-MODEL-EXACT-OCCUPANCY-CHAIN / CONDITIONAL"
        ),
        "theorem_problem_id": "M1 Cycle84 exact occupancy chain",
        "slot_table_digest": log_report["slot_table_digest"],
        "projected_log_certificate_sha256": log_report["certificate_sha256"],
        "full_replay_receipt_sha256": full_report["receipt_sha256"],
        "generated_source_sha256": source_report["source"]["sha256"],
        "finite_source_closure": {
            "algorithm_proof_status": algorithm_report["proof_status"],
            "algorithm_toy_model_count": len(algorithm_report["toy_models"]),
            "algorithm_circular_slice_cases": int(
                algorithm_report["circular_slice"]["cases_checked"]
            ),
            "source_contract_status": source_report["proof_status"],
            "source_line_count": int(source_report["source"]["line_count"]),
            "full_replay_status": full_report["proof_status"],
            "full_replay_threads": int(full_report["full_replay"]["threads"]),
        },
        "cycle84_exact": {
            "color_shell_size": shell_size,
            "projected_duplicate_bins": int(full_replay_data["duplicate_bins_replayed"]),
            "projected_half_domain_entries": int(full_replay_data["selected_entries"]),
            "true_double_fibers": true_double_fibers,
            "true_ordered_energy": true_energy,
            "m_max": exact_m_max,
            "no_fibers_of_size_at_least_3": True,
            "distinct_products": exact_occupancy,
        },
        "checks": checks,
        "remaining_import": (
            "reviewer acceptance of the finite-source closure audit for "
            "promotion beyond audit status"
        ),
        "imports_required": [
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    exact = report["cycle84_exact"]
    print("m1_cycle84_exact_occupancy_chain: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"slot_table_digest={report['slot_table_digest']}")
    print(f"projected_log_certificate_sha256={report['projected_log_certificate_sha256']}")
    print(f"full_replay_receipt_sha256={report['full_replay_receipt_sha256']}")
    print(f"generated_source_sha256={report['generated_source_sha256']}")
    closure = report["finite_source_closure"]
    print(
        "finite_source_closure="
        f"algorithm={closure['algorithm_proof_status']}, "
        f"toy_models={closure['algorithm_toy_model_count']}, "
        f"source_lines={closure['source_line_count']}, "
        f"full_replay={closure['full_replay_status']}"
    )
    print(
        "cycle84_exact="
        f"shell={exact['color_shell_size']}, "
        f"projected_bins={exact['projected_duplicate_bins']}, "
        f"double_fibers={exact['true_double_fibers']}, "
        f"energy={exact['true_ordered_energy']}, "
        f"m_max={exact['m_max']}, "
        f"distinct_products={exact['distinct_products']}"
    )
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 Cycle84 exact occupancy chain."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
