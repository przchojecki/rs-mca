#!/usr/bin/env python3
"""Verify the M1 Cycle120 support-wise MCA bridge.

The finite chain produces a support-wise line/MCA lower bound

    LD_sw(RS[F_17^32,H,256],262) >= N.

ABF Definition 4.3 consumes the normalized probability

    epsilon_mca(C,delta)

over a uniformly sampled line parameter.  This verifier checks the exact
definition-level conversion for the Cycle120 row: the same fixed line and N
distinct bad parameters give epsilon_mca(C,125/256) >= N/17^32, and this
density is strictly larger than 2^-128.
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

import verify_m1_cycle84_exact_occupancy_chain as cycle84
import verify_m1_cycle116_field_lift_contract as field_lift
import verify_m1_cycle120_gate_arithmetic as gate


EXPECTED_N = 52_747_567_092
EXPECTED_DELTA = "125/256"
EXPECTED_AGREEMENT = 262
EXPECTED_DOMAIN_SIZE = 512
EXPECTED_DIMENSION = 256
EXPECTED_FIELD_SIZE = 17**32
EPSILON_DEN_BITS = 128


def ceil_fraction(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise AssertionError("denominator must be positive")
    return (numerator + denominator - 1) // denominator


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    cycle84_report = local_reports.get("cycle84") or cycle84.build_report()
    lift_report = local_reports.get("field_lift") or field_lift.build_report()
    gate_report = local_reports.get("gate") or gate.build_report()

    exact = cycle84_report["cycle84_exact"]
    lift_field = lift_report["field"]
    lift_params = lift_report["parameters"]
    gate_object = gate_report["object"]
    gate_arithmetic = gate_report["arithmetic"]

    delta_num, delta_den = (int(part) for part in gate_object["delta"].split("/"))
    closed_threshold = ceil_fraction(
        (delta_den - delta_num) * int(gate_object["domain_size"]),
        delta_den,
    )
    bad_count = int(exact["distinct_products"])
    field_size = int(gate_object["field_size"])
    epsilon_denominator = 1 << EPSILON_DEN_BITS

    checks = {
        "cycle84_exact_chain_passes": cycle84_report["status"] == "PASS",
        "cycle116_lift_contract_passes": lift_report["status"] == "PASS",
        "cycle120_gate_arithmetic_passes": gate_report["status"] == "PASS",
        "same_bad_count_across_chain": (
            bad_count
            == int(lift_params["bad_gamma_count"])
            == int(gate_object["bad_gamma_count"])
            == EXPECTED_N
        ),
        "same_line_field_denominator_across_chain": (
            field_size
            == int(lift_field["lifted_field_size"])
            == EXPECTED_FIELD_SIZE
        ),
        "delta_matches_cycle120_row": gate_object["delta"] == EXPECTED_DELTA,
        "domain_and_dimension_match_cycle120_row": (
            int(gate_object["domain_size"]) == EXPECTED_DOMAIN_SIZE
            and int(gate_object["dimension"]) == EXPECTED_DIMENSION
            and int(lift_field["domain_size"]) == EXPECTED_DOMAIN_SIZE
            and int(lift_params["lift_dimension"]) == EXPECTED_DIMENSION
        ),
        "delta_is_subcapacity_for_rate_one_half": 2 * delta_num < delta_den,
        "closed_threshold_matches_agreement": (
            closed_threshold
            == int(gate_arithmetic["closed_agreement_threshold"])
            == int(lift_params["lift_agreement"])
            == EXPECTED_AGREEMENT
        ),
        "support_witnesses_meet_abf_closed_threshold": (
            int(lift_params["lift_agreement"]) >= closed_threshold
        ),
        "bad_count_is_valid_probability_numerator": 0 < bad_count <= field_size,
        "line_parameter_sampler_is_code_field": (
            gate_object["field"] == "F_17^32"
            and field_size == int(lift_field["lifted_field_size"])
        ),
        "density_exceeds_two_minus_128": (
            bad_count * epsilon_denominator > field_size
        ),
        "minimum_bad_count_gate_matches": (
            int(gate_arithmetic["minimum_bad_gamma_count_for_gt_2_minus_128"])
            == field_size // epsilon_denominator + 1
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / LD-SW-TO-EPSILON-MCA-BRIDGE",
        "theorem_problem_id": "M1 Cycle120 support-wise MCA bridge",
        "bridge_lemma": {
            "input": "LD_sw(C,a) >= M with one fixed line and distinct bad parameters",
            "condition": "a >= ceil((1-delta)n)",
            "output": "epsilon_mca(C,delta) >= M/|F|",
            "reason": (
                "epsilon_mca maximizes over fixed pairs (f1,f2) and samples "
                "the same line parameter uniformly from the code field"
            ),
        },
        "cycle120_instance": {
            "code": "RS[F_17^32,H,256]",
            "domain_size": EXPECTED_DOMAIN_SIZE,
            "dimension": EXPECTED_DIMENSION,
            "delta": gate_object["delta"],
            "closed_support_threshold": closed_threshold,
            "supportwise_agreement": int(lift_params["lift_agreement"]),
            "bad_parameters": bad_count,
            "line_field_size": field_size,
        },
        "mca_conclusion": {
            "statement": (
                "epsilon_mca(RS[F_17^32,H,256],125/256) "
                ">= 52747567092 / 17^32 > 2^-128"
            ),
            "numerator": bad_count,
            "denominator": field_size,
            "epsilon_star": f"2^-{EPSILON_DEN_BITS}",
            "minimum_bad_parameters_for_strict_gate": (
                field_size // epsilon_denominator + 1
            ),
        },
        "checks": checks,
        "remaining_imports": [
            "official ABF PDF/source verification for the row gates and "
            "Definition 4.3 wording",
            "reviewer acceptance of the Cycle84 generated source contract",
            "reviewer acceptance that the compact external Cycle116 contract "
            "faithfully records the hash-pinned PR #96 files",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    instance = report["cycle120_instance"]
    conclusion = report["mca_conclusion"]

    print("m1_cycle120_supportwise_mca_bridge: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "bridge="
        f"{report['bridge_lemma']['input']}; "
        f"{report['bridge_lemma']['condition']} => "
        f"{report['bridge_lemma']['output']}"
    )
    print(
        "cycle120_instance="
        f"{instance['code']}, n={instance['domain_size']}, "
        f"k={instance['dimension']}, delta={instance['delta']}, "
        f"threshold={instance['closed_support_threshold']}, "
        f"agreement={instance['supportwise_agreement']}"
    )
    print(
        "mca_lower_bound="
        f"{conclusion['numerator']} / {conclusion['denominator']} > "
        f"{conclusion['epsilon_star']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 Cycle120 LD_sw to epsilon_mca bridge."
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
