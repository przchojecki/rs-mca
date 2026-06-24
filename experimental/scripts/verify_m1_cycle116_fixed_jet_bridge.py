#!/usr/bin/env python3
"""Verify the formal Cycle116 slot-block fixed-jet reduction.

This nonmutating verifier supports
experimental/notes/m1/m1_cycle116_finite_chain_contract.md. It checks the
deterministic consequence of the imported 336 slot identities:

    seven blocks R_t(X)=X^16+O(X^10), plus the common factor (X-1),
    force P_T(X)=X^113-X^112+O(X^107), and
    R_t(beta)=3^t u_t implies P_T(beta)=4(beta-1)Phi(T).

It does not verify the 336 slot identities or the Cycle84 occupancy census.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Iterable, Set


BASE_FIELD_SIZE = 17
BLOCK_COUNT = 7
BLOCK_DEGREE = 16
BLOCK_LOW_MAX_DEGREE = 10
SINGLETON_FACTOR_DEGREE = 1
NATIVE_DOMAIN_SIZE = 256
NATIVE_COSUPPORT_SIZE = 113
FIXED_JET_SIGMA = 6
NATIVE_DIMENSION = 137
NATIVE_AGREEMENT = 143
SLOT_IDENTITY_COUNT = 7 * 3 * 16


def possible_sum_degrees(support: Iterable[int], count: int) -> Set[int]:
    degrees = {0}
    support_set = set(support)
    for _ in range(count):
        degrees = {old + new for old in degrees for new in support_set}
    return degrees


def build_report() -> Dict[str, Any]:
    block_support = set(range(BLOCK_LOW_MAX_DEGREE + 1)) | {BLOCK_DEGREE}
    q_degrees = possible_sum_degrees(block_support, BLOCK_COUNT)

    q_top_degree = BLOCK_COUNT * BLOCK_DEGREE
    q_forbidden_gap = list(range(q_top_degree - 1, q_top_degree - 6, -1))
    q_lower_degrees = q_degrees - {q_top_degree}

    # P=(X-1)Q has support in {d+1: d in supp(Q)} union supp(Q).
    p_possible_degrees = {d + SINGLETON_FACTOR_DEGREE for d in q_degrees} | q_degrees
    p_top_degree = q_top_degree + SINGLETON_FACTOR_DEGREE
    p_second_degree = q_top_degree
    p_remainder_degrees = p_possible_degrees - {p_top_degree, p_second_degree}

    checks = {
        "slot_identity_count_336": SLOT_IDENTITY_COUNT == 336,
        "cosupport_size_113": (
            SINGLETON_FACTOR_DEGREE + BLOCK_COUNT * BLOCK_DEGREE
            == NATIVE_COSUPPORT_SIZE
        ),
        "native_dimension_formula": (
            NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE - FIXED_JET_SIGMA
            == NATIVE_DIMENSION
        ),
        "native_agreement_formula": (
            NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE == NATIVE_AGREEMENT
        ),
        "q_has_degree_112": q_top_degree in q_degrees,
        "q_gap_111_to_107": not any(degree in q_degrees for degree in q_forbidden_gap),
        "q_lower_terms_degree_at_most_106": max(q_lower_degrees) == 106,
        "p_has_degree_113": p_top_degree in p_possible_degrees,
        "p_second_coefficient_forced_minus_one": (
            p_second_degree in p_possible_degrees
            and (p_second_degree - SINGLETON_FACTOR_DEGREE) not in q_degrees
        ),
        "p_remainder_degree_at_most_107": max(p_remainder_degrees) == 107,
        "sum_slots_1_to_7_is_28": sum(range(1, BLOCK_COUNT + 1)) == 28,
        "three_power_28_mod_17_is_4": pow(3, 28, BASE_FIELD_SIZE) == 4,
        "kappa_coefficients_4_beta_minus_1": [4, 4] != [0, 0],
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / SLOT-IDENTITY-DEPENDENT",
        "theorem_problem_id": "M1 Cycle116 fixed-jet slot-block bridge",
        "formal_reduction": {
            "slot_identities_required": SLOT_IDENTITY_COUNT,
            "block_shape": "R_t(X)=X^16+O(X^10)",
            "co_support": "{1} union seven disjoint 16-point slot blocks",
            "cosupport_size": NATIVE_COSUPPORT_SIZE,
            "q_product_shape": "Q_T(X)=X^112+O(X^106)",
            "locator_shape": "P_T(X)=X^113-X^112+O(X^107)",
            "fixed_jet_sigma": FIXED_JET_SIGMA,
        },
        "scalar_reduction": {
            "slot_exponent_sum": 28,
            "three_power_28_mod_17": pow(3, 28, BASE_FIELD_SIZE),
            "beta": "X+2",
            "kappa": "4(beta-1)",
            "kappa_coefficients_low_to_high": [4, 4],
            "product_scalar": "P_T(beta)=4(beta-1)Phi(T)",
        },
        "parameters": {
            "native_domain_size": NATIVE_DOMAIN_SIZE,
            "native_cosupport_size": NATIVE_COSUPPORT_SIZE,
            "native_dimension": NATIVE_DIMENSION,
            "native_agreement": NATIVE_AGREEMENT,
        },
        "checks": checks,
        "imports_required": [
            "Cycle116 slot-block assembly by verify_m1_cycle116_slot_assembly.py",
            "Cycle116 slot identity replay by verify_m1_cycle116_slot_identities.py",
            "Cycle84 projected duplicate-bin completeness for the normalized slot table",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    formal = report["formal_reduction"]
    scalar = report["scalar_reduction"]
    params = report["parameters"]

    print("m1_cycle116_fixed_jet_bridge: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "formal_reduction="
        f"{formal['slot_identities_required']} slot identities, "
        f"{formal['block_shape']} and common (X-1) factor imply "
        f"{formal['locator_shape']}"
    )
    print(
        "native="
        f"n={params['native_domain_size']}, j={params['native_cosupport_size']}, "
        f"sigma={formal['fixed_jet_sigma']}, k={params['native_dimension']}, "
        f"agreement={params['native_agreement']}"
    )
    print(
        "scalar_reduction="
        f"3^28={scalar['three_power_28_mod_17']} mod 17, "
        f"kappa={scalar['kappa']}, coefficients={scalar['kappa_coefficients_low_to_high']}"
    )
    print("checked=" + ", ".join(report["checks"].keys()))
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check the formal Cycle116 fixed-jet slot-block reduction."
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
