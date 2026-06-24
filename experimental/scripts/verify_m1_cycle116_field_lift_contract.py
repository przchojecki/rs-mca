#!/usr/bin/env python3
"""Check deterministic field/lift arithmetic for the Cycle116 M1 contract.

This verifier supports
experimental/notes/m1/m1_cycle116_finite_chain_contract.md. It checks the
finite-field envelope and parameter arithmetic used by the Cycle116 smooth
lift. The note proves the abstract smooth-padding lemma; this script checks
only its concrete Cycle116 field and cardinality hypotheses. It does not verify
the Cycle84 product census or fixed-jet identities.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Iterable, List, Sequence, Tuple


P = 17
EXTENSION_DEGREE = 16
MODULUS = [3] + [0] * 7 + [1] + [0] * 7 + [1]  # X^16 + X^8 + 3.

NATIVE_DOMAIN_SIZE = 256
NATIVE_COSUPPORT_SIZE = 113
FIXED_JET_SIGMA = 6
NATIVE_DIMENSION = 137
NATIVE_AGREEMENT = 143

ODD_PADDING_SIZE = 119
ODD_UNUSED_SIZE = 137
LIFT_DOMAIN_SIZE = 512
LIFT_DIMENSION = 256
LIFT_AGREEMENT = 262
DELTA_NUM = 125
DELTA_DEN = 256
BAD_GAMMA_COUNT = 52_747_567_092
EPSILON_DEN_BITS = 128

EXPECTED_F17_16 = 48_661_191_875_666_868_481
EXPECTED_F17_32 = 2_367_911_594_760_467_245_844_106_297_320_951_247_361


def trim(poly: Sequence[int]) -> List[int]:
    out = [c % P for c in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: Sequence[int], b: Sequence[int]) -> List[int]:
    size = max(len(a), len(b))
    return trim(
        [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(size)]
    )


def poly_sub(a: Sequence[int], b: Sequence[int]) -> List[int]:
    size = max(len(a), len(b))
    return trim(
        [(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(size)]
    )


def poly_mul(a: Sequence[int], b: Sequence[int]) -> List[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % P
    return trim(out)


def poly_divmod(a: Sequence[int], b: Sequence[int]) -> Tuple[List[int], List[int]]:
    divisor = trim(b)
    if not divisor:
        raise ZeroDivisionError("polynomial division by zero")

    remainder = trim(a)
    quotient = [0] * max(1, (len(remainder) - len(divisor) + 1))
    inv_lc = pow(divisor[-1], -1, P)

    while len(remainder) >= len(divisor) and remainder:
        shift = len(remainder) - len(divisor)
        coeff = remainder[-1] * inv_lc % P
        quotient[shift] = coeff
        for i, bi in enumerate(divisor):
            remainder[shift + i] = (remainder[shift + i] - coeff * bi) % P
        remainder = trim(remainder)

    return trim(quotient), remainder


def poly_mod(a: Sequence[int], modulus: Sequence[int]) -> List[int]:
    return poly_divmod(a, modulus)[1]


def poly_gcd(a: Sequence[int], b: Sequence[int]) -> List[int]:
    x = trim(a)
    y = trim(b)
    while y:
        _, r = poly_divmod(x, y)
        x, y = y, r
    if not x:
        return []
    inv_lc = pow(x[-1], -1, P)
    return [(coeff * inv_lc) % P for coeff in x]


def poly_pow_mod(base: Sequence[int], exponent: int, modulus: Sequence[int]) -> List[int]:
    result = [1]
    power = poly_mod(base, modulus)
    e = exponent
    while e:
        if e & 1:
            result = poly_mod(poly_mul(result, power), modulus)
        power = poly_mod(poly_mul(power, power), modulus)
        e >>= 1
    return result


def field_mul(a: Sequence[int], b: Sequence[int]) -> List[int]:
    return pad(poly_mod(poly_mul(a, b), MODULUS), EXTENSION_DEGREE)


def field_pow(base: Sequence[int], exponent: int) -> List[int]:
    result = [1] + [0] * (EXTENSION_DEGREE - 1)
    power = pad(poly_mod(base, MODULUS), EXTENSION_DEGREE)
    e = exponent
    while e:
        if e & 1:
            result = field_mul(result, power)
        power = field_mul(power, power)
        e >>= 1
    return result


def pad(poly: Sequence[int], size: int) -> List[int]:
    out = [c % P for c in poly[:size]]
    out.extend([0] * (size - len(out)))
    return out


def is_irreducible_modulus() -> bool:
    x = [0, 1]
    if poly_pow_mod(x, P**EXTENSION_DEGREE, MODULUS) != x:
        return False
    h = poly_sub(poly_pow_mod(x, P ** (EXTENSION_DEGREE // 2), MODULUS), x)
    return poly_gcd(MODULUS, h) == [1]


def coeffs_to_sparse(coeffs: Iterable[int]) -> Dict[str, int]:
    return {str(i): c for i, c in enumerate(coeffs) if c % P}


def build_report() -> Dict[str, Any]:
    one = [1] + [0] * (EXTENSION_DEGREE - 1)
    minus_one = [P - 1] + [0] * (EXTENSION_DEGREE - 1)
    eta = [0] * 9 + [6] + [0] * (EXTENSION_DEGREE - 10)

    field_size = P**EXTENSION_DEGREE
    lifted_field_size = field_size * field_size

    closed_threshold_num = (DELTA_DEN - DELTA_NUM) * LIFT_DOMAIN_SIZE
    if closed_threshold_num % DELTA_DEN != 0:
        raise AssertionError("lift threshold is not integral")
    closed_threshold = closed_threshold_num // DELTA_DEN

    checks = {
        "modulus_degree_16": len(trim(MODULUS)) - 1 == EXTENSION_DEGREE,
        "modulus_irreducible": is_irreducible_modulus(),
        "field_size_17_16": field_size == EXPECTED_F17_16,
        "eta_power_256_is_one": field_pow(eta, 256) == one,
        "eta_power_128_is_minus_one": field_pow(eta, 128) == minus_one,
        "eta_exact_order_256": field_pow(eta, 256) == one
        and field_pow(eta, 128) != one,
        "eta_nonsquare": field_pow(eta, (field_size - 1) // 2) == minus_one,
        "lifted_field_size_17_32": lifted_field_size == EXPECTED_F17_32,
        "theta_exact_order_512_follows": field_pow(eta, 256) == one
        and field_pow(eta, 128) == minus_one,
        "native_dimension_formula": (
            NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE - FIXED_JET_SIGMA
            == NATIVE_DIMENSION
        ),
        "native_agreement_formula": (
            NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT_SIZE == NATIVE_AGREEMENT
        ),
        "lift_agreement_padding": (
            NATIVE_AGREEMENT + ODD_PADDING_SIZE == LIFT_AGREEMENT
        ),
        "odd_coset_partition": (
            ODD_PADDING_SIZE + ODD_UNUSED_SIZE == NATIVE_DOMAIN_SIZE
        ),
        "lift_rate_one_half": 2 * LIFT_DIMENSION == LIFT_DOMAIN_SIZE,
        "closed_threshold_262": closed_threshold == LIFT_AGREEMENT,
        "bad_gamma_density_exceeds_2_minus_128": (
            BAD_GAMMA_COUNT * (1 << EPSILON_DEN_BITS) > lifted_field_size
        ),
        "floor_field_over_2_128_is_6": (
            lifted_field_size // (1 << EPSILON_DEN_BITS) == 6
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / FINITE-COMPUTATION-DEPENDENT",
        "theorem_problem_id": "M1 Cycle116 finite chain field/lift contract",
        "field": {
            "base": P,
            "modulus_sparse_coefficients": coeffs_to_sparse(MODULUS),
            "field_size": field_size,
            "eta_sparse_coefficients": coeffs_to_sparse(eta),
            "lifted_field_size": lifted_field_size,
            "theta_order": 512,
            "domain_size": LIFT_DOMAIN_SIZE,
        },
        "parameters": {
            "native_domain_size": NATIVE_DOMAIN_SIZE,
            "native_cosupport_size": NATIVE_COSUPPORT_SIZE,
            "fixed_jet_sigma": FIXED_JET_SIGMA,
            "native_dimension": NATIVE_DIMENSION,
            "native_agreement": NATIVE_AGREEMENT,
            "odd_padding_size": ODD_PADDING_SIZE,
            "odd_unused_size": ODD_UNUSED_SIZE,
            "lift_dimension": LIFT_DIMENSION,
            "lift_agreement": LIFT_AGREEMENT,
            "delta": f"{DELTA_NUM}/{DELTA_DEN}",
            "bad_gamma_count": BAD_GAMMA_COUNT,
        },
        "checks": checks,
        "imports_required": [
            "Cycle116 slot identity replay by verify_m1_cycle116_slot_identities.py",
            "Cycle84 projected duplicate-bin completeness for the normalized slot table",
            "Cycle116 slot-block assembly by verify_m1_cycle116_slot_assembly.py",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    field = report["field"]
    params = report["parameters"]

    print("m1_cycle116_field_lift_contract: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "field="
        f"F_{field['base']}^16 -> F_{field['base']}^32, "
        f"|K|={field['lifted_field_size']}, theta_order={field['theta_order']}"
    )
    print(
        "native="
        f"n={params['native_domain_size']}, j={params['native_cosupport_size']}, "
        f"sigma={params['fixed_jet_sigma']}, k={params['native_dimension']}, "
        f"agreement={params['native_agreement']}"
    )
    print(
        "lift="
        f"n={field['domain_size']}, k={params['lift_dimension']}, "
        f"agreement={params['lift_agreement']}, delta={params['delta']}"
    )
    print(
        "density_gate="
        f"{params['bad_gamma_count']} / {field['lifted_field_size']} > 2^-128"
    )
    print("checked=" + ", ".join(report["checks"].keys()))
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check field/lift arithmetic for the M1 Cycle116 contract."
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
