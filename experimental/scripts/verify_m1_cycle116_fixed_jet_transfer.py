#!/usr/bin/env python3
"""Verify the Cycle116 fixed-jet bad-parameter transfer algebra.

The slot-block bridge proves

    P_T(X)=X^113-X^112+O(X^107),
    P_T(beta)=4(beta-1) Phi(T).

This verifier checks the next algebraic step in the native Cycle116 line/MCA
transfer: the common top six coefficients of P_T force a common complement
locator truncation W, and the bad line parameter is

    z_T = W(beta) - V_D(beta)/P_T(beta).

Since V_D(beta) and 4(beta-1) are nonzero, distinct Phi(T) values give distinct
bad line parameters.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_fixed_jet_bridge as fixed_jet
import verify_m1_cycle116_slot_assembly as slot_assembly
import verify_m1_cycle116_slot_identities as slot_ids


NATIVE_DOMAIN_SIZE = 256
NATIVE_COSUPPORT_SIZE = 113
NATIVE_AGREEMENT = 143
FIXED_JET_SIGMA = 6
NATIVE_DIMENSION = 137


FieldElt = slot_ids.FieldElt
FieldPoly = List[FieldElt]


def trim(poly: Sequence[FieldElt]) -> FieldPoly:
    out = list(poly)
    while len(out) > 1 and out[-1] == slot_ids.ZERO:
        out.pop()
    return out


def degree(poly: Sequence[FieldElt]) -> int:
    return len(trim(poly)) - 1


def field_poly_sub(a: Sequence[FieldElt], b: Sequence[FieldElt]) -> FieldPoly:
    size = max(len(a), len(b))
    out = []
    for index in range(size):
        ai = a[index] if index < len(a) else slot_ids.ZERO
        bi = b[index] if index < len(b) else slot_ids.ZERO
        out.append(slot_ids.fsub(ai, bi))
    return trim(out)


def field_poly_eval(poly: Sequence[FieldElt], value: FieldElt) -> FieldElt:
    out = slot_ids.ZERO
    for coeff in reversed(poly):
        out = slot_ids.fadd(slot_ids.fmul(out, value), coeff)
    return out


def d0_locator_poly() -> FieldPoly:
    # D0=<eta> has exact order 256, so its locator is X^256-1.
    return [slot_ids.emb(-1)] + [slot_ids.ZERO] * (NATIVE_DOMAIN_SIZE - 1) + [
        slot_ids.ONE
    ]


def common_w_poly() -> FieldPoly:
    out = [slot_ids.ZERO] * (NATIVE_AGREEMENT + 1)
    for deg in range(NATIVE_DIMENSION + 1, NATIVE_AGREEMENT + 1):
        out[deg] = slot_ids.ONE
    return out


def complement_recurrence() -> list[int]:
    # P has top coefficients 1, -1, 0, 0, 0, 0 in degrees 113..108.
    p_top = [1, -1, 0, 0, 0, 0]
    l_top = [1]
    for r in range(1, FIXED_JET_SIGMA):
        total = 0
        for i in range(1, r + 1):
            total += p_top[i] * l_top[r - i]
        l_top.append((-total) % slot_ids.P)
    return l_top


def field_inverse(value: FieldElt) -> FieldElt:
    if value == slot_ids.ZERO:
        raise ZeroDivisionError("cannot invert zero")
    return slot_ids.fpow(value, slot_ids.FIELD_SIZE - 2)


def representative_phi() -> FieldElt:
    beta_squared = slot_ids.fmul(slot_ids.BETA, slot_ids.BETA)
    seed_polys = {
        seed: slot_ids.prime_poly_from_roots(
            pow(3, exponent, slot_ids.P) for exponent in exponents
        )
        for seed, exponents in slot_ids.E_SETS.items()
    }
    out = slot_ids.ONE
    for t in slot_assembly.ACTIVE_COSETS:
        out = slot_ids.fmul(
            out,
            slot_ids.normalized_u(seed_polys, beta_squared, t, 1, 0),
        )
    return out


def representative_native_polys() -> tuple[FieldPoly, FieldPoly, FieldPoly]:
    h32 = slot_assembly.h32_elements()
    choices = tuple((1, 0) for _ in slot_assembly.ACTIVE_COSETS)
    roots, product, direct = slot_assembly.locator_product_from_blocks(choices, h32)
    if product != direct:
        raise AssertionError("representative direct locator mismatch")

    complement_roots = sorted(slot_assembly.d0_elements() - roots)
    complement = slot_ids.poly_from_roots(complement_roots)
    return product, complement, d0_locator_poly()


def build_report() -> Dict[str, Any]:
    fixed_report = fixed_jet.build_report()
    p_poly, l_poly, vd_poly = representative_native_polys()
    w_poly = common_w_poly()
    q_poly = field_poly_sub(w_poly, l_poly)

    p_times_l = slot_assembly.field_poly_mul(p_poly, l_poly)

    beta = slot_ids.BETA
    beta_minus_one = slot_ids.fsub(beta, slot_ids.ONE)
    kappa = slot_ids.fmul(slot_ids.emb(4), beta_minus_one)
    phi = representative_phi()

    p_beta = field_poly_eval(p_poly, beta)
    l_beta = field_poly_eval(l_poly, beta)
    vd_beta = field_poly_eval(vd_poly, beta)
    w_beta = field_poly_eval(w_poly, beta)
    q_beta = field_poly_eval(q_poly, beta)
    z_by_fraction = slot_ids.fsub(
        w_beta,
        slot_ids.fmul(vd_beta, field_inverse(p_beta)),
    )

    recurrence = complement_recurrence()
    expected_top = [1] * FIXED_JET_SIGMA

    checks = {
        "fixed_jet_bridge_passes": fixed_report["status"] == "PASS",
        "native_parameters_match": (
            NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE - FIXED_JET_SIGMA
            == NATIVE_DIMENSION
            and NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE == NATIVE_AGREEMENT
        ),
        "complement_recurrence_top_six_all_one": recurrence == expected_top,
        "common_w_has_degrees_138_to_143": (
            degree(w_poly) == NATIVE_AGREEMENT
            and all(
                w_poly[deg] == slot_ids.ONE
                for deg in range(NATIVE_DIMENSION + 1, NATIVE_AGREEMENT + 1)
            )
            and all(w_poly[deg] == slot_ids.ZERO for deg in range(NATIVE_DIMENSION + 1))
        ),
        "representative_p_has_required_fixed_jet": (
            degree(p_poly) == NATIVE_COSUPPORT_SIZE
            and p_poly[NATIVE_COSUPPORT_SIZE] == slot_ids.ONE
            and p_poly[NATIVE_COSUPPORT_SIZE - 1] == slot_ids.emb(-1)
            and all(
                p_poly[deg] == slot_ids.ZERO
                for deg in range(
                    NATIVE_COSUPPORT_SIZE - FIXED_JET_SIGMA + 1,
                    NATIVE_COSUPPORT_SIZE - 1,
                )
            )
        ),
        "representative_complement_has_common_w_truncation": (
            degree(l_poly) == NATIVE_AGREEMENT
            and all(
                l_poly[deg] == slot_ids.ONE
                for deg in range(NATIVE_DIMENSION + 1, NATIVE_AGREEMENT + 1)
            )
        ),
        "q_polynomial_degree_at_most_native_dimension": (
            degree(q_poly) <= NATIVE_DIMENSION
        ),
        "representative_product_times_complement_is_d0_locator": (
            p_times_l == vd_poly
        ),
        "beta_outside_d0": slot_ids.fpow(beta, NATIVE_DOMAIN_SIZE) != slot_ids.ONE,
        "vd_beta_nonzero": vd_beta != slot_ids.ZERO,
        "kappa_nonzero": kappa != slot_ids.ZERO,
        "p_beta_nonzero": p_beta != slot_ids.ZERO,
        "field_inverses_check": (
            slot_ids.fmul(vd_beta, field_inverse(vd_beta)) == slot_ids.ONE
            and slot_ids.fmul(kappa, field_inverse(kappa)) == slot_ids.ONE
            and slot_ids.fmul(p_beta, field_inverse(p_beta)) == slot_ids.ONE
        ),
        "representative_scalar_identity": (
            p_beta == slot_ids.fmul(kappa, phi)
        ),
        "representative_z_formula_matches_q_beta": q_beta == z_by_fraction,
        "noncontainment_degree_inequality": (
            NATIVE_AGREEMENT == NATIVE_DIMENSION + FIXED_JET_SIGMA
            and NATIVE_AGREEMENT > NATIVE_DIMENSION
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / FIXED-JET-TRANSFER-ALGEBRA",
        "theorem_problem_id": "M1 Cycle116 fixed-jet bad-parameter transfer",
        "transfer": {
            "native_domain_locator": "V_D(X)=X^256-1",
            "co_support_locator_shape": "P_T(X)=X^113-X^112+O(X^107)",
            "complement_locator_truncation": (
                "W(X)=X^143+X^142+X^141+X^140+X^139+X^138"
            ),
            "code_dimension": NATIVE_DIMENSION,
            "agreement": NATIVE_AGREEMENT,
            "bad_parameter_formula": (
                "z_T=W(beta)-V_D(beta)/P_T(beta)"
            ),
            "scalar_substitution": (
                "P_T(beta)=4(beta-1)Phi(T), with V_D(beta) and 4(beta-1) nonzero"
            ),
            "injectivity_reason": (
                "Phi -> W(beta)-V_D(beta)/(4(beta-1)Phi) is injective on "
                "nonzero Phi values"
            ),
            "noncontainment_reason": (
                "(X-beta)G+1 has degree <=137, vanishes on 143 points, "
                "and equals 1 at beta"
            ),
        },
        "representative_check": {
            "tuple_choices": [
                {"t": t, "seed": 1, "shift": 0}
                for t in slot_assembly.ACTIVE_COSETS
            ],
            "p_degree": degree(p_poly),
            "complement_degree": degree(l_poly),
            "q_degree": degree(q_poly),
            "p_beta_equals_kappa_phi": True,
            "z_formula_matches_q_beta": True,
        },
        "checks": checks,
        "imports_required": [
            "Cycle116 slot identity replay for the fixed-jet and scalar identity",
            "Cycle84 exact occupancy for the number of distinct Phi(T) values",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    transfer = report["transfer"]
    rep = report["representative_check"]

    print("m1_cycle116_fixed_jet_transfer: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "transfer="
        f"{transfer['native_domain_locator']}, "
        f"{transfer['co_support_locator_shape']} => "
        f"{transfer['complement_locator_truncation']}"
    )
    print(
        "bad_parameter_map="
        f"{transfer['bad_parameter_formula']}; "
        f"{transfer['scalar_substitution']}"
    )
    print(
        "representative="
        f"P_degree={rep['p_degree']}, L_degree={rep['complement_degree']}, "
        f"Q_degree={rep['q_degree']}, scalar={rep['p_beta_equals_kappa_phi']}, "
        f"z={rep['z_formula_matches_q_beta']}"
    )
    print(f"injectivity={transfer['injectivity_reason']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle116 fixed-jet bad-parameter transfer algebra."
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
