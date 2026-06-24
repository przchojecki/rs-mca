#!/usr/bin/env python3
"""Verify the reviewer-facing M1 Cycle120 obstruction theorem ledger.

This verifier does not introduce new arithmetic. It checks that the current
local proof layers compose into one source-conditioned obstruction theorem for
the Cycle120 row, while keeping the official ABF-source and finite-source
promotion gates explicit.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle120_abf_extract_sources as abf_extract
import verify_m1_cycle120_end_to_end_chain as end_to_end


EXPECTED_N = 52_747_567_092
EXPECTED_FIELD_SIZE = 17**32
EXPECTED_DELTA = "125/256"
EXPECTED_CLOSED_AGREEMENT = 262
EXPECTED_STRICT_AGREEMENT = 263
EXPECTED_STRICT_DISTANCE = 249
EPSILON_DEN_BITS = 128


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    chain_report = local_reports.get("end_to_end") or end_to_end.build_report()
    source_report = local_reports.get("abf_extract") or abf_extract.build_report()

    chain = chain_report["chain"]
    cycle84 = chain["cycle84_exact_occupancy"]
    native = chain["cycle116_native"]
    lifted = chain["cycle116_smooth_lift"]
    mca = chain["cycle120_supportwise_mca"]
    gate = chain["cycle120_gate_arithmetic"]
    field_ledger = chain["cycle120_domain_field_ledger"]
    fixed_theorem = chain["fixed_jet_ldsw_theorem"]
    padding_theorem = chain["smooth_padding_ldsw_theorem"]
    two_ended_theorem = chain["two_ended_fixed_jet_ldsw_theorem"]

    numerator = int(mca["numerator"])
    denominator = int(mca["denominator"])
    epsilon_denominator = 1 << EPSILON_DEN_BITS

    checks = {
        "end_to_end_chain_passes": chain_report["status"] == "PASS",
        "abf_extract_source_audit_passes": source_report["status"] == "PASS",
        "cycle84_numerator_matches_expected": (
            int(cycle84["distinct_products"]) == EXPECTED_N
        ),
        "native_cycle116_ldsw_statement_matches_chain": (
            native["conclusion"] == "LD_sw(RS[F0,D0,137],143) >= N"
            and int(native["agreement"]) == 143
            and int(native["bad_line_parameters"]) == EXPECTED_N
        ),
        "cycle120_closed_ldsw_statement_matches_chain": (
            lifted["conclusion"] == "LD_sw(RS[F_17^32,H,256],262) >= N"
            and int(lifted["agreement"]) == EXPECTED_CLOSED_AGREEMENT
            and int(lifted["bad_line_parameters"]) == EXPECTED_N
        ),
        "definition_bridge_matches_cycle120_row": (
            numerator == EXPECTED_N
            and denominator == EXPECTED_FIELD_SIZE
            and mca["epsilon_star"] == f"2^-{EPSILON_DEN_BITS}"
        ),
        "density_strictly_exceeds_gate": (
            numerator * epsilon_denominator > denominator
            and int(gate["minimum_bad_gamma_count_for_gt_2_minus_128"]) == 7
        ),
        "closed_threshold_is_262": (
            int(gate["closed_agreement_threshold"]) == EXPECTED_CLOSED_AGREEMENT
        ),
        "field_ledgers_are_identical": (
            int(field_ledger["q_gen"])
            == int(field_ledger["q_code"])
            == int(field_ledger["q_line"])
            == EXPECTED_FIELD_SIZE
        ),
        "proof_logic_theorems_are_present": (
            fixed_theorem["proof_status"]
            == "PROVED / AUDIT / GENERIC-FIXED-JET-LDSW-THEOREM"
            and padding_theorem["proof_status"]
            == "PROVED / AUDIT / SMOOTH-PADDING-LDSW-THEOREM"
            and two_ended_theorem["proof_status"]
            == "PROVED / AUDIT / TWO-ENDED-FIXED-JET-LDSW-THEOREM"
        ),
        "strict_ball_addendum_is_recorded": (
            int(two_ended_theorem["agreement"]) == EXPECTED_STRICT_AGREEMENT
            and int(two_ended_theorem["distance"]) == EXPECTED_STRICT_DISTANCE
            and two_ended_theorem["strict_delta_bound"] == "249/512"
            and int(two_ended_theorem["bad_parameters"]) == EXPECTED_N
        ),
        "abf_extract_has_source_pages": set(
            int(page) for page in source_report["rendered_source_pages"].keys()
        )
        == {5, 9, 17},
        "abf_extract_keeps_official_review_open": any(
            "official ePrint" in item
            for item in source_report["remaining_imports"]
        ),
        "finite_source_promotion_boundary_is_open": any(
            "Cycle84" in item and "finite-source" in item
            for item in chain_report["remaining_imports"]
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": (
            "CONDITIONAL / AUDIT / CYCLE120-FINITE-OBSTRUCTION-THEOREM"
        ),
        "theorem_problem_id": "M1 Cycle120 finite obstruction theorem ledger",
        "conditional_theorem": {
            "row": "C=RS[F_17^32,H,256], H=<theta>, |H|=512",
            "delta": EXPECTED_DELTA,
            "epsilon_star": f"2^-{EPSILON_DEN_BITS}",
            "statement": (
                "subject to official ABF source agreement and finite-source "
                "review, epsilon_mca(C,125/256) >= 52747567092/17^32 > 2^-128"
            ),
            "closed_threshold_input": (
                "LD_sw(RS[F_17^32,H,256],262) >= 52747567092"
            ),
            "strict_ball_addendum": (
                "LD_sw(RS[F_17^32,H,256],263) >= 52747567092"
            ),
        },
        "numerics": {
            "bad_parameters": numerator,
            "line_field_size": denominator,
            "minimum_bad_parameters_for_gt_2_minus_128": int(
                gate["minimum_bad_gamma_count_for_gt_2_minus_128"]
            ),
            "closed_agreement_threshold": int(gate["closed_agreement_threshold"]),
            "strict_distance": int(two_ended_theorem["distance"]),
        },
        "proof_layers": {
            "cycle84_exact_occupancy": cycle84,
            "fixed_jet_ldsw_theorem": fixed_theorem,
            "smooth_padding_ldsw_theorem": padding_theorem,
            "two_ended_fixed_jet_ldsw_theorem": two_ended_theorem,
            "field_ledger": field_ledger,
            "supportwise_mca_bridge": mca,
        },
        "source_condition": {
            "abf_extract_status": source_report["proof_status"],
            "abf_pdf_sha256": source_report["source"]["files"]["abf_pdf"]["sha256"],
            "source_commit": source_report["source"]["head_commit"],
            "rendered_source_pages": source_report["rendered_source_pages"],
        },
        "remaining_imports": [
            "independent official ABF ePrint PDF/source fetch and revision check",
            "reviewer acceptance of the Cycle84 finite-source closure audit",
            "official review of external PR #96 provenance if cited directly",
        ],
        "checks": checks,
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    theorem = report["conditional_theorem"]
    numerics = report["numerics"]
    source = report["source_condition"]

    print("m1_cycle120_obstruction_theorem: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"row={theorem['row']}")
    print(
        "closed_threshold="
        f"{theorem['closed_threshold_input']}, delta={theorem['delta']}"
    )
    print(f"conclusion={theorem['statement']}")
    print(
        "strict_ball_addendum="
        f"{theorem['strict_ball_addendum']}, "
        f"distance={numerics['strict_distance']}"
    )
    print(
        "density_gate="
        f"N={numerics['bad_parameters']}, |F|={numerics['line_field_size']}, "
        f"minimum_for_gate="
        f"{numerics['minimum_bad_parameters_for_gt_2_minus_128']}"
    )
    print(
        "abf_extract="
        f"{source['abf_extract_status']}, "
        f"commit={source['source_commit']}, "
        f"pdf_sha256={source['abf_pdf_sha256']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 Cycle120 obstruction theorem ledger."
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
