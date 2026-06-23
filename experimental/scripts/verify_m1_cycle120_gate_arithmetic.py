#!/usr/bin/env python3
"""Verify the arithmetic layer of the M1 Cycle120 gate contract.

This is a nonmutating audit script for
experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md. It checks only
deterministic integer arithmetic and parameter-envelope predicates. It does
not verify the Cycle84 finite count, the Cycle116/Cycle119 transfer proofs, or
the official ABF source text.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any, Dict


BASE_FIELD_SIZE = 17
EXTENSION_DEGREE = 32
DOMAIN_SIZE = 512
DIMENSION = 256
DELTA_NUM = 125
DELTA_DEN = 256
EPSILON_DEN_BITS = 128
BAD_GAMMA_COUNT = 52_747_567_092
CYCLE116_AGREEMENT = 262
CYCLE119_AGREEMENT = 263
FIELD_ENVELOPE_BITS = 256
DEGREE_ENVELOPE_BITS = 40

EXPECTED_FIELD_SIZE = 2_367_911_594_760_467_245_844_106_297_320_951_247_361

IMPORTS_REQUIRED = (
    "official ABF source gates and page references",
    "finite certificate for K, theta, and H=<theta>",
    "Cycle84 finite energy/census producing N",
    "Cycle116 finite-chain transfer at agreement 262",
    "optional Cycle119 two-ended transfer at agreement 263",
)


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def build_report() -> Dict[str, Any]:
    field_size = BASE_FIELD_SIZE**EXTENSION_DEGREE
    epsilon_denominator = 1 << EPSILON_DEN_BITS

    threshold_num = (DELTA_DEN - DELTA_NUM) * DOMAIN_SIZE
    if threshold_num % DELTA_DEN != 0:
        raise AssertionError("closed agreement threshold is not integral")
    closed_agreement_threshold = threshold_num // DELTA_DEN

    radius_num = DELTA_NUM * DOMAIN_SIZE
    if radius_num % DELTA_DEN != 0:
        raise AssertionError("distance radius is not integral")
    distance_radius = radius_num // DELTA_DEN

    strict_distance = DOMAIN_SIZE - CYCLE119_AGREEMENT
    strict_delta = Fraction(strict_distance, DOMAIN_SIZE)
    cycle119_closed_threshold = DOMAIN_SIZE - strict_distance

    checks = {
        "field_size_matches": field_size == EXPECTED_FIELD_SIZE,
        "field_within_2_256": field_size < (1 << FIELD_ENVELOPE_BITS),
        "degree_within_2_40": DIMENSION <= (1 << DEGREE_ENVELOPE_BITS),
        "domain_power_of_two": is_power_of_two(DOMAIN_SIZE),
        "rate_one_half": 2 * DIMENSION == DOMAIN_SIZE,
        "closed_threshold_agreement_262": closed_agreement_threshold == 262,
        "cycle116_meets_closed_threshold": (
            CYCLE116_AGREEMENT >= closed_agreement_threshold
        ),
        "distance_radius_250": distance_radius == 250,
        "cycle119_distance_strictly_inside_radius": (
            strict_distance < distance_radius
        ),
        "cycle119_closed_threshold_matches_249_over_512": (
            cycle119_closed_threshold == CYCLE119_AGREEMENT
            and strict_delta == Fraction(249, 512)
        ),
        "floor_field_over_2_128_is_6": (
            field_size // epsilon_denominator == 6
        ),
        "bad_gamma_density_exceeds_2_minus_128": (
            BAD_GAMMA_COUNT * epsilon_denominator > field_size
        ),
    }

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / SOURCE-CHECK-NEEDED",
        "theorem_problem_id": "M1 corrected MCA / Cycle120 ABF gate audit",
        "object": {
            "field": f"F_{BASE_FIELD_SIZE}^{EXTENSION_DEGREE}",
            "field_size": field_size,
            "domain_size": DOMAIN_SIZE,
            "dimension": DIMENSION,
            "rate": "1/2",
            "delta": f"{DELTA_NUM}/{DELTA_DEN}",
            "epsilon_star": f"2^-{EPSILON_DEN_BITS}",
            "bad_gamma_count": BAD_GAMMA_COUNT,
        },
        "arithmetic": {
            "closed_agreement_threshold": closed_agreement_threshold,
            "distance_radius": distance_radius,
            "cycle116_agreement": CYCLE116_AGREEMENT,
            "cycle119_agreement": CYCLE119_AGREEMENT,
            "cycle119_distance": strict_distance,
            "cycle119_delta_bound": (
                f"{strict_delta.numerator}/{strict_delta.denominator}"
            ),
            "floor_field_over_2_128": field_size // epsilon_denominator,
            "minimum_bad_gamma_count_for_gt_2_minus_128": (
                field_size // epsilon_denominator + 1
            ),
        },
        "checks": checks,
        "imports_required": list(IMPORTS_REQUIRED),
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    obj = report["object"]
    arithmetic = report["arithmetic"]

    print("m1_cycle120_gate_arithmetic: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "object="
        f"{obj['field']}, n={obj['domain_size']}, k={obj['dimension']}, "
        f"rate={obj['rate']}, delta={obj['delta']}"
    )
    print(f"field_size={obj['field_size']}")
    print(
        "closed_agreement_threshold="
        f"{arithmetic['closed_agreement_threshold']}"
    )
    print(f"distance_radius={arithmetic['distance_radius']}")
    print(
        "cycle116="
        f"agreement {arithmetic['cycle116_agreement']} meets closed threshold"
    )
    print(
        "cycle119="
        f"agreement {arithmetic['cycle119_agreement']} gives distance "
        f"{arithmetic['cycle119_distance']} and delta*_C <= "
        f"{arithmetic['cycle119_delta_bound']}"
    )
    print(
        "density_gate="
        f"{obj['bad_gamma_count']} / {obj['field_size']} > "
        f"{obj['epsilon_star']}"
    )
    print("checked=" + ", ".join(report["checks"].keys()))
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Check deterministic arithmetic for the M1 Cycle120 gate contract."
        )
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
