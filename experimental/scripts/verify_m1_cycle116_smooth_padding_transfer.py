#!/usr/bin/env python3
"""Verify the concrete Cycle116 smooth-padding transfer.

The native row gives

    LD_sw(RS[F0,D0,137],143) >= N.

The Cycle116 smooth lift adjoins theta with theta^2=eta, takes
H=<theta>=D0 disjoint_union theta D0, and partitions the odd coset as

    A={theta eta^i: 0<=i<=118},
    R={theta eta^i: 119<=i<=255}.

This verifier checks the concrete padding facts used to preserve the same bad
parameters in the [512,256] row: A supplies 119 forced agreement points, R is
the fixed co-support padding, P_R(beta) is nonzero, and the fixed-jet degree
loss remains sigma=6 after multiplying by the fixed R-locator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_field_lift_contract as field_lift
import verify_m1_cycle116_fixed_jet_transfer as fixed_transfer
import verify_m1_cycle116_slot_identities as slot_ids


NATIVE_DOMAIN_SIZE = 256
NATIVE_AGREEMENT = 143
NATIVE_DIMENSION = 137
NATIVE_COSUPPORT_SIZE = 113
FIXED_JET_SIGMA = 6

A_START = 0
A_END = 118
R_START = 119
R_END = 255

LIFT_DOMAIN_SIZE = 512
LIFT_COSUPPORT_SIZE = 250
LIFT_DIMENSION = 256
LIFT_AGREEMENT = 262
DELTA = "125/256"


FieldElt = slot_ids.FieldElt
KElt = Tuple[FieldElt, FieldElt]

K_ZERO: KElt = (slot_ids.ZERO, slot_ids.ZERO)
K_ONE: KElt = (slot_ids.ONE, slot_ids.ZERO)
K_MINUS_ONE: KElt = (slot_ids.emb(-1), slot_ids.ZERO)
K_THETA: KElt = (slot_ids.ZERO, slot_ids.ONE)
K_BETA: KElt = (slot_ids.BETA, slot_ids.ZERO)


def ksub(a: KElt, b: KElt) -> KElt:
    return (slot_ids.fsub(a[0], b[0]), slot_ids.fsub(a[1], b[1]))


def kmul(a: KElt, b: KElt) -> KElt:
    # (a0+a1 theta)(b0+b1 theta), theta^2=eta.
    constant = slot_ids.fadd(
        slot_ids.fmul(a[0], b[0]),
        slot_ids.fmul(slot_ids.fmul(a[1], b[1]), slot_ids.ETA),
    )
    theta_coeff = slot_ids.fadd(
        slot_ids.fmul(a[0], b[1]),
        slot_ids.fmul(a[1], b[0]),
    )
    return (constant, theta_coeff)


def kpow(base: KElt, exponent: int) -> KElt:
    out = K_ONE
    power = base
    e = exponent
    while e:
        if e & 1:
            out = kmul(out, power)
        power = kmul(power, power)
        e >>= 1
    return out


def d0_elements() -> List[KElt]:
    return [
        (slot_ids.fpow(slot_ids.ETA, exponent), slot_ids.ZERO)
        for exponent in range(NATIVE_DOMAIN_SIZE)
    ]


def odd_coset_elements() -> List[KElt]:
    return [
        (slot_ids.ZERO, slot_ids.fpow(slot_ids.ETA, exponent))
        for exponent in range(NATIVE_DOMAIN_SIZE)
    ]


def inclusive_odd_slice(start: int, end: int) -> List[KElt]:
    return [
        (slot_ids.ZERO, slot_ids.fpow(slot_ids.ETA, exponent))
        for exponent in range(start, end + 1)
    ]


def product_at_beta(roots: Iterable[KElt]) -> KElt:
    out = K_ONE
    for root in roots:
        out = kmul(out, ksub(K_BETA, root))
    return out


def build_report() -> Dict[str, Any]:
    field_report = field_lift.build_report()
    transfer_report = fixed_transfer.build_report()

    d0 = d0_elements()
    odd = odd_coset_elements()
    h = d0 + odd
    a_points = inclusive_odd_slice(A_START, A_END)
    r_points = inclusive_odd_slice(R_START, R_END)

    a_set = set(a_points)
    r_set = set(r_points)
    d0_set = set(d0)
    odd_set = set(odd)
    h_set = set(h)

    p_a_beta = product_at_beta(a_points)
    p_r_beta = product_at_beta(r_points)

    native_fixed_gap_bound = NATIVE_COSUPPORT_SIZE - FIXED_JET_SIGMA
    lifted_fixed_gap_bound = R_END - R_START + 1 + native_fixed_gap_bound

    checks = {
        "field_lift_contract_passes": field_report["status"] == "PASS",
        "native_fixed_transfer_passes": transfer_report["status"] == "PASS",
        "theta_square_is_eta": kmul(K_THETA, K_THETA)
        == (slot_ids.ETA, slot_ids.ZERO),
        "theta_order_512": (
            kpow(K_THETA, 512) == K_ONE
            and kpow(K_THETA, 256) == K_MINUS_ONE
        ),
        "H_size_512": len(h_set) == LIFT_DOMAIN_SIZE,
        "H_partitions_even_and_odd_cosets": (
            len(d0_set) == NATIVE_DOMAIN_SIZE
            and len(odd_set) == NATIVE_DOMAIN_SIZE
            and d0_set.isdisjoint(odd_set)
            and h_set == d0_set | odd_set
        ),
        "A_and_R_partition_odd_coset": (
            len(a_set) == R_START - A_START
            and len(r_set) == R_END - R_START + 1
            and a_set.isdisjoint(r_set)
            and a_set | r_set == odd_set
        ),
        "A_disjoint_from_native_support": a_set.isdisjoint(d0_set),
        "R_disjoint_from_native_cosupport": r_set.isdisjoint(d0_set),
        "beta_not_in_H": K_BETA not in h_set,
        "padding_locators_nonzero_at_beta": (
            p_a_beta != K_ZERO and p_r_beta != K_ZERO
        ),
        "lift_cosupport_size_250": (
            NATIVE_COSUPPORT_SIZE + len(r_set) == LIFT_COSUPPORT_SIZE
        ),
        "lift_agreement_size_262": (
            NATIVE_AGREEMENT + len(a_set) == LIFT_AGREEMENT
        ),
        "lift_dimension_256": NATIVE_DIMENSION + len(a_set) == LIFT_DIMENSION,
        "same_fixed_sigma_after_R_padding": (
            lifted_fixed_gap_bound == LIFT_COSUPPORT_SIZE - FIXED_JET_SIGMA
            == 244
        ),
        "explaining_codeword_degree_bound": (
            (NATIVE_DIMENSION - 1) + len(a_set) < LIFT_DIMENSION
        ),
        "noncontainment_division_returns_native_degree": (
            (LIFT_DIMENSION - 1) - len(a_set) < NATIVE_DIMENSION
        ),
        "closed_threshold_matches_delta": (
            DELTA == field_report["parameters"]["delta"]
            and LIFT_AGREEMENT == int(field_report["parameters"]["lift_agreement"])
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / SMOOTH-PADDING-TRANSFER",
        "theorem_problem_id": "M1 Cycle116 smooth [512,256] padding transfer",
        "smooth_padding": {
            "field": "K=F0(theta), theta^2=eta",
            "domain": "H=<theta>=D0 disjoint_union theta D0",
            "A_range": [A_START, A_END],
            "A_size": len(a_set),
            "R_range": [R_START, R_END],
            "R_size": len(r_set),
            "native_agreement": NATIVE_AGREEMENT,
            "lift_agreement": LIFT_AGREEMENT,
            "native_dimension": NATIVE_DIMENSION,
            "lift_dimension": LIFT_DIMENSION,
            "native_cosupport_size": NATIVE_COSUPPORT_SIZE,
            "lift_cosupport_size": LIFT_COSUPPORT_SIZE,
            "fixed_jet_sigma": FIXED_JET_SIGMA,
            "delta": DELTA,
            "P_A_beta_nonzero": True,
            "P_R_beta_nonzero": True,
        },
        "transfer": {
            "bad_parameters_preserved": True,
            "support_formula": "S_T^+=(D0\\J_T) union A",
            "cosupport_formula": "J_T^+=J_T union R",
            "explaining_codeword_degree": (
                "deg(L_A c_z) <= 118+136 < 256"
            ),
            "noncontainment_division": (
                "degree <256 codewords vanishing on A divide by L_A and "
                "return degree <137 native codewords"
            ),
            "fixed_jet_degree_bound": (
                "deg(P_R(P_T-P_T')) <= 137+107=244=250-6"
            ),
            "product_scalar_preserved": (
                "P_T^+(beta)=P_R(beta)P_T(beta), with P_R(beta) nonzero"
            ),
        },
        "checks": checks,
        "imports_required": [
            "native Cycle116 fixed-jet transfer at agreement 143",
            "Cycle84 exact occupancy for the bad-parameter count",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    padding = report["smooth_padding"]
    transfer = report["transfer"]

    print("m1_cycle116_smooth_padding_transfer: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "domain="
        f"{padding['domain']}, A={padding['A_range']} size {padding['A_size']}, "
        f"R={padding['R_range']} size {padding['R_size']}"
    )
    print(
        "lift="
        f"agreement {padding['native_agreement']}+{padding['A_size']}="
        f"{padding['lift_agreement']}, dimension {padding['lift_dimension']}, "
        f"cosupport {padding['lift_cosupport_size']}"
    )
    print(
        "degree_bounds="
        f"{transfer['explaining_codeword_degree']}; "
        f"{transfer['fixed_jet_degree_bound']}"
    )
    print(f"noncontainment={transfer['noncontainment_division']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle116 smooth-padding transfer."
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
